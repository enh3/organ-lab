from pyo import *
import numpy as np

# These functions are called when Notein receives a MIDI note event.
def noteon(voice):
    "Print pitch and velocity for noteon event."
    pit = int(note["pitch"].get(all=True)[voice])
    vel = int(note["velocity"].get(all=True)[voice] * 127)
    print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))


def noteoff(voice):
    "Print pitch and velocity for noteoff event."
    pit = int(note["pitch"].get(all=True)[voice])
    vel = int(note["velocity"].get(all=True)[voice] * 127)
    print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))
    


s = Server()
s.setMidiInputDevice(99)
s.boot()
partials = list(range(1, 8, 1))
mul = [(0.5**i)*0.25 for i in range(7)]#numpy.logspace(0.5, 0.0000025, 4) 
note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

note.keyboard()

tfon = TrigFunc(note["trigon"], noteon, arg=list(range(10)))
adsr = MidiAdsr(note['velocity'], attack=0.001, decay=0.1, sustain=0.7, release=0.5)

freq = MToF(note["pitch"])

amps = Port(note["velocity"], risetime=0.005, falltime=0.5, mul=0.1)

#tfon = TrigFunc(note["trigon"], noteon, arg=list(range(10)))
#adsr = MidiAdsr(note['velocity'], attack=0.01, decay=0, sustain=1, release=0.01)

#freqlist = [Sig(notes["pitch"]*i) for i in range(4)] # signals wih values 100, 150, etc. and the LFO added 



pitch = [(partial * freq) for partial in partials]
print(pitch)
#lfMul = [(1/i)*10 for i in freq]
#lf = Sine(0.5, mul=lfMul)

sound = [Sine(freq=pit, mul=amp * adsr) for pit, amp in zip(pitch, mul)]
#a = Sine(freq=freq, mul=amps)
SL = Mix(sound, 1).out()
SR = Mix(sound, 1).out(1)

# TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
# contains 10 streams, there will be 10 caller, each one with its own argument,
# taken from the list of integers given at `arg` argument.
tfon = TrigFunc(note["trigon"], noteon, arg=list(range(10)))
tfoff = TrigFunc(note["trigoff"], noteoff, arg=list(range(10)))

s.gui(locals())