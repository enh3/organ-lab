from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
import keyboard

s = Server()
s.setMidiInputDevice(99)
s.boot()

#muls = [1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0]

class Stop :
    def __init__(self, part, mul, att, rel, rand):
        self.note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
        self.note.keyboard()
        self.partials = part
        self.muls = mul
        self.attacks = att
        self.releases = rel
        self.rand = rand
        self.freq = MToF(self.note['pitch'])
        self.pitch = [(partial * self.freq) for partial in self.partials]
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=0.001, decay=0.146, sustain=0.70, release=0.1)
        self.noise = PinkNoise(0.7) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.freq*(20/4)), q=10, mul=.4)
        self.noise = Mix(self.noise, 1)
        self.sound = [Sine(freq=pit, mul=amp*MidiAdsr(self.note['velocity'], attack=attacks, decay=0, sustain=1, release=releases)) for pit, amp, attacks, releases in zip(self.pitch, self.muls, self.attacks, self.releases)]
        self.sound = Mix(self.sound, 1)
        self.mix = STRev(self.sound+self.noise, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
    def out(self):
        "Sends the synth's signal to the audio output and return the object itself."
        self.mix.out()
        return self
        
#bourdon = Stop([1, 0.01, 0.5], [1, 1, 1], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1], .1).out()

bourdon = Stop([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], .1).out()

#note = NoteinSustain(scale=0)


#sound = STRev(Mix(p1, 1), inpos=0.5, revtime=5, cutoff=4000, bal=0.15)


'''
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
'''
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
#pp = Print(transV, interval=0.1, message="Audio stream value")

s.amp = 0.3

s.start()
s.gui(locals())