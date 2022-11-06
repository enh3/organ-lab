from pyo import *
from random import random


s = Server()
s.setMidiInputDevice(99)
s.boot()

class Stop:
    def __init__(self, part, mul, att, rel, rand, trans):
        # scale=1 to get pitch values in hertz
        self.note = Notein(poly=10, scale=1, first=0, last=127, channel=0, mul=1)
        self.note.keyboard()
        self.ampsOrigin = []
        self.amps = []
        self.envs = []
        self.snds = []
        self.mixed = []
        self.trans = []
        self.call = TrigFunc(self.note["trigon"], self.ampsScale, arg=list(range(10)))
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=0.001, decay=0.146, sustain=0.70, release=0.1)
        self.noise = PinkNoise(1.5) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.note['pitch']*(20/4)), q=10, mul=.4)
        self.noise = Mix(self.noise, 1)
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # SigTo to avoid clicks
            self.ampsOrigin.append(SigTo(mul[i], time=0.025))
            self.amps.append(SigTo(mul[i], time=0.025))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=0, sustain=1, release=rel[i], mul=self.amps[-1]))
            self.trans.append(SigTo(trans[i], time=0.025))
            self.snds.append(Sine(freq=part[i] * self.note['pitch'] + Randi(-rand, rand, 5) + self.trans[-1], mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())

        self.mix = STRev(sum(self.mixed)+self.noise, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)

    def out(self):
        self.mix.out()
        return self

    def setMuls(self, x):
        for i in range(len(self.ampsOrigin)):
            self.ampsOrigin[i].value = x[i]
            
    def setTrans(self, x):
        for i in range(len(self.trans)):
            self.trans[i].value = x[i]
            
    def vel(self):
        return self.note['velocity']
        
    def ampsScale(self, voice):
        freq = self.note.get("pitch", all=True)[voice]
        stretch_factor = rescale(freq, xmin=20, xmax=20000, ymin=1, ymax=0.5, xlog=True, ylog=True)
        for i in range(len(self.amps)):
            self.amps[i].value = self.ampsOrigin[i].value * ((stretch_factor**(((i+1)/2)+0.5))/stretch_factor)
            print(i, '=', self.amps[i].value)
       

def bourdon():
    stop1.setMuls([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    
def principal():
    stop1.setMuls([1, 0.4, 0.3, 0.2, 0.2, 0.08, 0.04, 0.06, 0.004, 0.003, 0.003, 0.003, 0.003, 0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])

def randGen():
    stop1.setMuls([random(), random()*0.5, random()*0.3, random()*0.2, random()*0.1, random()*0.05, random()*0.03, random()*0.01, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005])
    
glissC = [0 for i in range(21)]

def gliss():
    global glissC
    print(glissC)
    if glissC[0] < 200:
        stop1.setTrans(glissC)
        for i in range(len(glissC)):
            if i % 2 == 0:
                glissC[i] = glissC[i] + 2
            else:
                glissC[i] = glissC[i] + -2
    else:
        for i in range(len(glissC)):
            glissC[i] = 0

'''
def dissocie(x):
    print("test")
    
  
'''

dissCount = 0
def dissocie(x):
    global dissCount
    print(x)
    if x != 0:
        dissCount += 1
        print(dissCount)
        if dissCount > 1:
            stop1.setMuls([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            print("set0")
        elif dissCount == 1 :
            stop1.setMuls([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
            print("setnon0")
    if dissCount == 4:
        dissCount = 0


partList = list(range(1, 21, 1))
transList = list(range(1, 21, 1))

i = 0

def stateChanges(address, *args):
    global i, stopV
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    if i == 1:
        bourdon()
    elif i == 2:
        principal()
    elif i == 3:
        randP.play()
    elif i == 4:
        randP.stop()
        glissP.play()
    elif i == 5:
        trigDiss.setThreshold(0)

scan = OscDataReceive(port=9002, address="*", function=stateChanges)

stop1 = Stop(partList, [1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 2, transList).out()

stopV = stop1.vel()
dummy = Sig(0)
trigDiss = Thresh(stop1.vel(), threshold=100, dir=0)

randP = Pattern(function=randGen, time=3)
glissP = Pattern(function=gliss, time=0.1)
diss = Pattern(function=dissocie, time=0.5)
tr = TrigFunc(trigDiss, function=dissocie, arg=stop1.vel())

s.amp = 0.3

s.start()
s.gui(locals())