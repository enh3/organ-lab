from pyo import *

s = Server()
s.setMidiInputDevice(99)
s.boot()

randDev = Sig(1)
transV = Sig(0)

p1Mul = Sig(1)
p2Mul = Sig(0.2)
p3Mul = Sig(0.5)
p4Mul = Sig(0.01)

note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
note.keyboard()

p1Env = MidiAdsr(note['velocity'], attack=0.1, decay=0.02, sustain=0.3, release=0.1, mul=p1Mul)
p2Env = MidiAdsr(note['velocity'], attack=0.25, decay=0.04, sustain=0.2, release=0.1, mul=p2Mul)
p3Env = MidiAdsr(note['velocity'], attack=0.05, decay=0.01, sustain=0.1, release=0.1, mul=p3Mul)
p4Env = MidiAdsr(note['velocity'], attack=0.07, decay=0.008, sustain=0.05, release=0.1, mul=p4Mul)

noiseEnv = MidiAdsr(note['velocity'], attack=0.001, decay=0.146, sustain=0.07, release=0.1)

freq = MToF(note['pitch'])

noise = PinkNoise(0.7) * noiseEnv
noise = Reson(noise, freq=(freq*(20/4)), q=10)

p1 = Sine(freq=freq+Randi(-randDev, randDev, 5)+transV, mul=p1Env)
p2= Sine(freq=(freq*2)+Randi(-randDev, randDev, 5)+transV, mul=p2Env)
p3 = Sine(freq=(freq*3)+Randi(-randDev, randDev, 5)+transV, mul=p3Env)
p4 = Sine(freq=(freq*4)+Randi(-randDev, randDev, 5)-transV, mul=p4Env)

sound = STRev(Mix(p1+p2+p3+p4+noise, 1), inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
SL = Mix(sound, 1).out()
SR = Mix(sound, 1).out(1)

p1Mul.ctrl(title="p1Mul")
p2Mul.ctrl(title="p2Mul")
p3Mul.ctrl(title="p3Mul")
p4Mul.ctrl(title="p4Mul")
p1Env.ctrl(title="p1Env")
p2Env.ctrl(title="p2Env")
p3Env.ctrl(title="p3Env")
p4Env.ctrl(title="p4Env")
noise.ctrl(title="Noise")
noiseEnv.ctrl(title="Noise Envelope")

'''
def trans():
    transV.value = Adsr(attack=240, release=10, mul=1000).play()

transEnv = Pattern(trans, 120).play()
'''
#Fader se comporte pas comme attendu avec le méthode .range, donnant 0.5 à 1 pour .range(0, 1) par example
'''  
def bToD():
    p1Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(1, 0.635).play()#.635
    p2Mul.value = Fader(fadein=2, fadeout=2, dur=4, mul=1, add=0).range(0.2, 0.823).play()#.723
    p3Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(0.3, 0.515).play()#.515
    p4Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(0.01, 0.535).play()#.535


bourdToDiap = Pattern(bToD, 4).play()
'''
pp = Print(transV, interval=0.1, message="Audio stream value")

s.amp = 0.3

s.start()
s.gui(locals())