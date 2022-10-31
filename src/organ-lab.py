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
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # To avoid clicks, you can use SigTo!
            self.amps.append(SigTo(mul[i], time=0.025))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=0, sustain=1, release=rel[i], mul=self.amps[-1]))
            self.snds.append(Sine(freq=part[i] * self.note['pitch'], mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())

        self.mix = STRev(sum(self.mixed), inpos=0.5, revtime=5, cutoff=4000, bal=0.15)


    def out(self):
        self.mix.out()
        return self

    def setMuls(self, x):
        for i in range(len(self.amps)):
            self.amps[i].value = x[i]
       
def amplitudes():
    bourdon.setMuls([random(), random()*0.5, random()*0.3, random()*0.2])

   
#pat2 = Pattern(function=amplitudes, time=1).play()

#muls is the second element here ([1, 0, 0, 0])
bourdon = Stop([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]).out()

s.amp = 0.3

s.start()
s.gui(locals())