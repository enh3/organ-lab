from pyo import *
import numpy as np

s = Server()
s.setMidiInputDevice(99)
s.boot()
partials = list(range(1, 8, 1))
mul = [(0.4**i)*0.0625 for i in range(7)]
note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

note.keyboard()

env = MidiAdsr(note['velocity'], attack=0.003, decay=0.1, sustain=0.7, release=0.5)
noiseEnv = MidiAdsr(note['velocity'], attack=0.001, decay=0.01, sustain=0.1, release=0.1)

fEnv = LinTable([(0,15000), (100,10000)])

def fEnvDef():
    print('trig')
    fEnv.play()

freq = MToF(note["pitch"])
pitch = note['pitch']
trig = Change(freq)
TrigFunc(trig, fEnvDef)


pitchTest = note['pitch']
trig = Change(pitchTest)
filtEnv = TrigEnv(trig, table=fEnv, dur=5)
pp = Print(filtEnv, interval=0.001, message="Audio stream value")


amps = Port(note["velocity"], risetime=0.005, falltime=0.5, mul=0.1)

pitch = [(partial * freq) for partial in partials]

#lfMul = [(1/i)*10 for i in freq]
#lf = Sine(0.5, mul=lfMul)

sound = [Sine(freq=pit+Randi(-2.0, 2.0, 5), mul=amp*env) + BrownNoise(0.02) * noiseEnv for pit, amp in zip(pitch, mul)]
sound = STRev(Mix(sound, 1), inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
sound = ButLP(sound, filtEnv)

SL = sound.out()
SR = sound.out(1)

s.start()
s.gui(locals())
