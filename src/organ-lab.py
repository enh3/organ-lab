from pyo import *

s = Server()
s.setMidiInputDevice(99)
s.boot()


partialsInit = [1]
mul = [1]
randDev = Sig(1)
note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
note.keyboard()

env = MidiAdsr(note['velocity'], attack=0.03, decay=0.1, sustain=0.8, release=0.5)
noiseEnv = MidiAdsr(note['velocity'], attack=0.001, decay=0.146, sustain=0.158, release=0.1)
print(s.getNumberOfStreams())
p1Env = MidiAdsr(note['velocity'], attack=0.1, decay=0.01, sustain=0.1, release=0.1)
p2Env = MidiAdsr(note['velocity'], attack=5, decay=0.01, sustain=0.2, release=0.1)
p3Env = MidiAdsr(note['velocity'], attack=5, decay=0.01, sustain=0.2, release=0.1)
p4Env = MidiAdsr(note['velocity'], attack=5, decay=0.01, sustain=0.2, release=0.1)
t = HarmTable([1]+[0.07]+[0.01]+[0.003]+[0]*20, size=512)
t.autoNormalize(True)
t.view()
t.graph()


freq = MToF(note['pitch'])
pitch = [(partial * freq) for partial in partialsInit]

noise = PinkNoise(25) * noiseEnv
noise = Reson(noise, freq=(freq*(20/4)), q=10)

partEnvs = [p1Env, p2Env, p3Env, p4Env]

sound = [Osc(t, freq=pit+Randi(-randDev, randDev, 5), mul=amp*env) for pit, amp in zip(pitch, mul)]
sound = STRev(Mix(sound, 1) + noise, inpos=0.5, revtime=1, cutoff=4000, bal=0.15)
sound = ButLP(sound, freq=1650)


noise.ctrl(title="Noise")
env.ctrl(title="Harmonics Envelope")
noiseEnv.ctrl(title="Noise Envelope")

def new():
    randDev.value = Adsr(attack=240, release=10, mul=1000).play()
    
"""
< 30:
        randDev.value += 1
    else:
        randDev.value -= 1
    return(randDev)
"""

randDevEnv = Pattern(new, 120).play()

pp = Print(randDev, interval=0.1, message="Audio stream value")

SL = sound.out()
SR = sound.out(1)

print(randDev)

s.noteout(pitch=1, velocity=20)
s.amp = 0.03

s.start()
s.gui(locals())
