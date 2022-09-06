from pyo import *
import numpy as np

s = Server()
s.setMidiInputDevice(99)
s.boot()
t = HarmTable([1]+[0]*24, size=512)
t.autoNormalize(True)
t.view()
t.graph()
partialsInit = [1] #list(range(1, 8, 1))
mul = [(0.3**i)*0.0625 for i in range(7)]
note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

note.keyboard()

env = MidiAdsr(note['velocity'], attack=0.03, decay=0.1, sustain=0.8, release=0.5)
noiseEnv = MidiAdsr(note['velocity'], attack=0.001, decay=0.1, sustain=0.2, release=0.1)
p1Env = MidiAdsr(note['velocity'], attack=0.001, decay=0.01, sustain=0.1, release=0.1)
p2Env = MidiAdsr(note['velocity'], attack=0.01, decay=0.01, sustain=0.2, release=0.1)

freq = MToF(note['pitch'])

pitch = [(partial * freq) for partial in partialsInit]

noiseGen = PinkNoise(5) * noiseEnv
noise1 = Reson(noiseGen, freq=freq*1, q=4)
noise2 = Reson(noiseGen, freq=(freq*(10/4)), q=4)
noise3 = Reson(noiseGen, freq=(freq*(20/4)), q=10)
noise4 = Reson(noiseGen, freq=freq*4, q=4)
noise5 = Reson(noiseGen, freq=freq*5, q=4)
noise6 = Reson(noiseGen, freq=freq*6, q=4)
part = Sine(freq=400, mul=mul*env)
part2 = part * pitch
a = [Osc(t, freq=pit+Randi(-3.0, 3.0, 5), mul=env*amp) for pit, amp in zip(pitch, mul)]
sound = STRev(Mix(a, 1) + noise3, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
sound = ButLP(sound, freq=1650)

noise1.ctrl(title="Noise1")
noise2.ctrl(title="Noise2")
noise3.ctrl(title="Noise3")
noise4.ctrl(title="Noise4")
part.ctrl(title="Mul")
env.ctrl(title="Envelope")
noiseEnv.ctrl(title="Noise Envelope")

SL = sound.out()
SR = sound.out(1)

s.start()
s.gui(locals())
