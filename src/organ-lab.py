from pyo import *
import numpy as np

s = Server()
s.setMidiInputDevice(99)
s.boot()
partialsInit = list(range(1, 8, 1))
mul = [(0.3**i)*0.0625 for i in range(7)]
#mul[0], mul[1] = mul[1], mul[0]
print(mul)
note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

note.keyboard()

env = MidiAdsr(note['velocity'], attack=0.003, decay=0.1, sustain=0.7, release=0.5)
noiseEnv = MidiAdsr(note['velocity'], attack=0.001, decay=0.01, sustain=0.1, release=0.1)
p1Env = MidiAdsr(note['velocity'], attack=0.001, decay=0.01, sustain=0.1, release=0.1)
p2Env = MidiAdsr(note['velocity'], attack=0.01, decay=0.01, sustain=0.2, release=0.1)

freq = MToF(note['pitch'])

#amps = Port(note["velocity"], risetime=0.005, falltime=0.5, mul=0.1)

pitch = [(partial * freq) for partial in partialsInit]

#lfMul = [(1/i)*10 for i in freq]
#lf = Sine(0.5, mul=lfMul)

noise = PinkNoise(0.8) * noiseEnv
noise = Reson(noise, freq=freq*4, q=4)
noise2 = Reson(noise, freq=freq*6, q=4)
partialsSynth = [Sine(freq=pit+Randi(-2.0, 2.0, 5), mul=amp*env) for pit, amp in zip(pitch, mul)]
sound = STRev(Mix(partialsSynth, 1) + noise + noise2, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)

noise.ctrl(title="Noise")
mul.ctrl(title="Mul")

SL = sound.out()
SR = sound.out(1)

s.start()
s.gui(locals())
