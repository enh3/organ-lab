import sys, time, multiprocessing
from pyo import *


VOICES_PER_CORE = 4
#First four partials in the harmonic series
partList = list(range(1, 4, 1))

if sys.platform.startswith("linux"):
    audio = "jack"
elif sys.platform.startswith("darwin"):
    audio = "portaudio"
else:
    print("Multicore examples don't run under Windows... Sorry!")
    exit()
    
class Stop(multiprocessing.Process):
    def __init__(self, pipe, part, mul):
        super(Stop, self).__init__()
        self.daemon = True
        self.pipe = pipe
        self.part = []
        self.amps = []
        self.envs = []
        self.snds = []
        self.mixed = []
        self.part = part
        self.mul = mul

    def run(self):
        self.server = Server(audio=audio)
        self.server.deactivateMidi()
        self.server.boot().start()
        self.mid = Notein(poly=VOICES_PER_CORE, scale=1, first=0, last=127)
        # Handles the user polyphony independently to avoid mixed polyphony concerns
        for i in range(len(self.part)):
            self.amps.append(Sig(self.mul[i]))
            self.envs.append(MidiAdsr(self.mid['velocity'], attack=.01, decay=.1, sustain=.8, release=.5, mul=self.amps[-1]))
            self.part.append(Sig(self.part[i]))
            self.snds.append(Sine(freq=(self.part[i]) * (MToF(FToM(self.mid['pitch']))), mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix1 = Mix(self.mixed, voices=1, mul=1).out(0)
        self.mix2 = Mix(self.mixed, voices=1, mul=1).out(1)

        while True:
            if self.pipe.poll():
                message = self.pipe.recv()
                command, data = message  # Unpack the message into command and data
                print(command, *data, flush=True)
                if command == 'setMul':
                    self.setMul(*data)  # Call setMul with the list of new values
                elif command == 'midiEvent':
                    try:
                        self.server.addMidiEvent(*data)  # Unpack the MIDI data and call addMidiEvent
                    except Exception as e:
                        print(f"Error processing MIDI event: {e}")

        self.server.stop()
        
    def setMul(self, x):
        for i in range(len(self.amps)):
            self.amps[i].value = x[i]

if __name__ == "__main__":
    main1, child1 = multiprocessing.Pipe()
    main2, child2 = multiprocessing.Pipe()
    main3, child3 = multiprocessing.Pipe()
    main4, child4 = multiprocessing.Pipe()
    mains = [main1, main2, main3, main4]
    p1 = Stop(child1, partList, [1, 0, 0, 0])
    p2 = Stop(child2, partList, [1, 0, 0, 0])
    p3 = Stop(child3, partList, [1, 0, 0, 0])
    p4 = Stop(child4, partList, [1, 0, 0, 0])
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.setMul([1, 1, 1, 1])
    p2.setMul([1, 1, 1, 1])
    p3.setMul([1, 1, 1, 1])
    p4.setMul([1, 1, 1, 1])

    playing = {0: [], 1: [], 2: [], 3: []}
    currentcore = 0

    def callback(status, data1, data2):
        global currentcore
        if status == 0x80 or status == 0x90 and data2 == 0:
            for i in range(4):
                if data1 in playing[i]:
                    playing[i].remove(data1)
                    mains[i].send(('midiEvent', (status, data1, data2)))
                    break
        elif status == 0x90:
            for i in range(4):
                currentcore = (currentcore + 1) % 4
                if len(playing[currentcore]) < VOICES_PER_CORE:
                    playing[currentcore].append(data1)
                    mains[currentcore].send(('midiEvent', (status, data1, data2)))
                    break
                    
    def setMul():
        global p1, p2, p3, p4
        new_values = [1, 1, 1, 1]
        for i in range(4):
            mains[i].send(('setMul', [new_values]))

    s = Server()
    s.setOutputDevice(1)
    s.setMidiInputDevice(99)
    s.boot()
    s.amp = 0.05
    s.start()
    raw = RawMidi(callback)
    setMul()
    s.gui(locals())

