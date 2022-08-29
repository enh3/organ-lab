from pyo import *
import numpy as np
s = Server()
s.setMidiInputDevice(99)
s.boot()

note = Notein(poly=10, scale=0, first=0, last=127)
note.keyboard()

tfon = TrigFunc(note["trigon"], noteon, arg=list(range(10)))
adsr = MidiAdsr(note['velocity'], attack=0.01, decay=0, sustain=1, release=0.01)

amps = Port(note["velocity"], risetime=0.005, falltime=0.5, mul=0.1)
#partials = [0.5, 1.5, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0]
#freqlist = [Sig(notes["pitch"]*i) for i in range(4)] # signals wih values 100, 150, etc. and the LFO added 
partials = list(range(1, 8, 1))
freq = MToF(note["pitch"])
pitch = [(partial * freq) for partial in partials]
print(pitch)
#lfMul = [(1/i)*10 for i in freq]
#lf = Sine(0.5, mul=lfMul)
mul = [(0.5**i)*0.25 for i in range(7)]#numpy.logspace(0.5, 0.0000025, 4)
a = Sine(freq=pitch, mul=0.002)
f = Mix(a, 2).out()

# These functions are called when Notein receives a MIDI note event.
def noteon(voice):
    "Print pitch and velocity for noteon event."
    pit = int(notes["pitch"].get(all=True)[voice])
    vel = int(notes["velocity"].get(all=True)[voice] * 127)
    print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))


def noteoff(voice):
    "Print pitch and velocity for noteoff event."
    pit = int(notes["pitch"].get(all=True)[voice])
    vel = int(notes["velocity"].get(all=True)[voice] * 127)
    print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))
    
# TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
# contains 10 streams, there will be 10 caller, each one with its own argument,
# taken from the list of integers given at `arg` argument.
tfon = TrigFunc(notes["trigon"], noteon, arg=list(range(10)))
tfoff = TrigFunc(notes["trigoff"], noteoff, arg=list(range(10)))

s.gui(locals())