from pyo import *
from random import random


s = Server()
s.setMidiInputDevice(99)
s.boot()
       
class Stop:
    def __init__(self, part, mul, att, rel):
        # scale=1 to get pitch values in hertz
        self.note = Notein(poly=10, scale=1, first=0, last=127, channel=0, mul=1)
        self.note.keyboard()

        self.amps = []
        self.envs = []
        self.snds = []
        self.mixed = []
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=0.001, decay=0.146, sustain=0.70, release=0.1)
        self.noise = PinkNoise(1.5) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.note['pitch']*(20/4)), q=10, mul=.4)
        self.noise = Mix(self.noise, 1)
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # SigTo to avoid clicks
            self.amps.append(SigTo(mul[i], time=0.025))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=0, sustain=1, release=rel[i], mul=self.amps[-1]))
            self.snds.append(Sine(freq=part[i] * self.note['pitch'], mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())

        self.mix = STRev(sum(self.mixed)+self.noise, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)


    def out(self):
        self.mix.out()
        return self

    def setMuls(self, x):
        for i in range(len(self.amps)):
            self.amps[i].value = x[i]
       

def bourdon():
    global i
    stop1.setMuls([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    
def principal():
    global i
    stop1.setMuls([1, 0.4, 0.3, 0.2, 0.2, 0.08, 0.04, 0.06, 0.004, 0.003, 0.003, 0.003, 0.003, 0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])

def randGen():
    stop1.setMuls([random(), random()*0.5, random()*0.3, random()*0.2, random()*0.1, random()*0.05, random()*0.03, random()*0.01, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005])
    

partList = list(range(1, 21, 1))

i = 0

pat = Pattern(function=randGen, time=3)

def stateChanges(address, *args):
    global i
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    if i == 1:
        bourdon()
    elif i == 2:
        principal()
    elif i == 3:
        pat.play()

scan = OscDataReceive(port=9002, address="*", function=stateChanges)

stop1 = Stop(partList, [1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]).out()

s.amp = 0.3

s.start()
s.gui(locals())