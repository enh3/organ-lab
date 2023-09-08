from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain

s = Server()
s.setMidiInputDevice(99)
s.boot()

randDev = Sig(1)
transV = Sig(0)

p1Mul = Sig(0.5) #.588
p2Mul = Sig(0.5) #.062
p3Mul = Sig(0.5) #.412
p4Mul = Sig(0) #.010
p5Mul = Sig(0)# .092
p6Mul = Sig(0)# .092

note = NoteinSustain(scale=0)
#note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
#note.keyboard()

p1Env = MidiAdsr(note['velocity'], attack=0.2, decay=0.2, sustain=0.2, release=0.2, mul=p1Mul)
p2Env = MidiAdsr(note['velocity'], attack=0.2, decay=0.2, sustain=0.2, release=0.2, mul=p2Mul)
p3Env = MidiAdsr(note['velocity'], attack=0.2, decay=0.2, sustain=0.2, release=0.2, mul=p3Mul)
p4Env = MidiAdsr(note['velocity'], attack=0.073, decay=0.008, sustain=0.05, release=0.1, mul=p4Mul)
p5Env = MidiAdsr(note['velocity'], attack=0.088, decay=0.008, sustain=0.05, release=0.1, mul=p5Mul)
p6Env = MidiAdsr(note['velocity'], attack=0.088, decay=0.008, sustain=0.05, release=0.1, mul=p6Mul)

noiseEnv = MidiAdsr(note['velocity'], attack=0.05, decay=0.05, sustain=0.05, release=0.05, mul=0)

freq = MToF(note['pitch'])

noise = PinkNoise(0.7) * noiseEnv
noise = Reson(noise, freq=(freq*(20/4)), q=10, mul=.4)

p1 = Sine(freq=freq+Randi(-randDev, randDev, 5)+transV, mul=p1Env)
p2= Sine(freq=(freq*2)+Randi(-randDev, randDev, 5)+transV, mul=p2Env)
p3 = Sine(freq=(freq*3)+Randi(-randDev, randDev, 5)+transV, mul=p3Env)
p4 = Sine(freq=(freq*4)+Randi(-randDev, randDev, 5)-transV, mul=p4Env)
p5 = Sine(freq=(freq*5)+Randi(-randDev, randDev, 5)-transV, mul=p5Env)
p6 = Sine(freq=(freq*6)+Randi(-randDev, randDev, 5)-transV, mul=p6Env)

sound = STRev(Mix(p1+p2+p3+p4+p5+p6+noise, 1), inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
SL = Mix(sound, 1).out()
SR = Mix(sound, 1).out(1)

p1Mul.ctrl(title="p1Mul")
p2Mul.ctrl(title="p2Mul")
p3Mul.ctrl(title="p3Mul")
p4Mul.ctrl(title="p4Mul")
p5Mul.ctrl(title="p5Mul")
p6Mul.ctrl(title="p6Mul")
p1Env.ctrl(title="p1Env")
p2Env.ctrl(title="p2Env")
p3Env.ctrl(title="p3Env")
p4Env.ctrl(title="p4Env")
p5Env.ctrl(title="p5Env")
p6Env.ctrl(title="p6Env")
noise.ctrl(title="Noise")
noiseEnv.ctrl(title="Noise Envelope")

#pp = Print(transV, interval=0.1, message="Audio stream value")

sp = Spectrum(SL, size=8192)

s.amp = 0.2

s.start()
s.gui(locals())





