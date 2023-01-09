from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
from random import random

#pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(1)
s.setMidiInputDevice(0)
s.boot()

class Stop:
    def __init__(self, part, partScRat, mul, att, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseMul, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index):
        # scale=1 to get pitch values in hertz
        self.note = Notein(poly=10, scale=1, first=0, last=127, channel=0)
        self.note.keyboard()
        self.ramp = Sig(ramp)
        self.fmMul = Sig(fmMul)
        self.noiseAtt = Sig(noiseAtt)
        self.noiseDec = Sig(noiseDec)
        self.noiseSus = Sig(noiseSus)
        self.noiseRel = Sig(noiseRel)
        self.noiseMul = Sig(noiseMul)
        self.noiseFiltQ = Sig(noiseFiltQ)
        self.amps = []
        self.envs = []
        self.part = []
        self.snds = []
        self.mixed = []
        self.trans = []
        self.velocity = [Clip(Sig(v), max=0.01, mul=100) for v in self.note['velocity']]
        self.partScRat = [(0,partScRat), (2,1)]
        self.partSc = MidiLinseg(self.velocity, self.partScRat)
        #self.partScRat = Sig(partScRat)
        #self.partSc = SigTo(1, time=4, init=self.partScRat.value)
        self.pp = Print(self.partSc, interval=0.3, message="Audio stream value")
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=self.noiseAtt.value, decay=self.noiseDec.value, sustain=self.noiseSus.value, release=self.noiseRel.value)
        self.noise = PinkNoise(1.5) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.note['pitch']*(20/4)), q=self.noiseFiltQ)
        self.noise = Mix(self.noise, 1, mul=self.noiseMul)
        self.fmEnv = MidiAdsr(self.note['trigon'], attack=0.001, decay=2, sustain=0.30, release=2)
        #self.fm1 = FM(carrier=self.note['pitch']*4, ratio=0.43982735, index=2.11232, mul=self.fmEnv)
        #self.fm2 = FM(carrier=self.fm1, ratio=0.72348, index=1.376, mul=self.fmEnv)
        self.fmod = self.note['pitch'] * ratio
        self.amod = self.fmod * index
        self.mod = Sine(self.fmod, mul=self.amod)
        #self.pp = Print(self.partScale, interval=0.3, message="Audio stream value")
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # SigTo to avoid clicks
            self.amps.append(SigTo(mul[i], time=self.ramp))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=0, sustain=1, release=rel[i], mul=self.amps[-1]))
            self.trans.append(SigTo(trans[i], time=0.025))
            self.part.append(SigTo(part[i], time=0.2))
            self.snds.append(Sine(freq=(self.part[i]**self.partSc) * self.note['pitch'] + Randi(-rand, rand, 5) + self.trans[-1] + self.mod, mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=1)
        self.sp = Spectrum(self.mix)
        self.filt = ButLP(self.mix+self.noise, 2000)
        self.rev = STRev(self.filt, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
        #self.tf = TrigFunc(self.note["trigon"], function=self.resetPartSc) # Notein.poly defaults to 10

    def out(self):
        self.rev.out()
        return self
        
    def setEnvAtt(self, x):
        for i in range(len(self.envs)):
            self.envs[i].setAttack(x[i])
            
    def setEnvDec(self, x):
        for i in range(len(self.envs)):
            self.envs[i].setDecay(x[i])
            
    def setEnvSus(self, x):
        for i in range(len(self.envs)):
            self.envs[i].setSustain(x[i])
            
    def setEnvRel(self, x):
        for i in range(len(self.envs)):
            self.envs[i].setRelease(x[i])
        
    def resetPartSc(self):
        self.partSc.setTime = 0.2
        self.partSc.value = self.partScRat
        self.partSc.setTim = 5
        self.partSc.value = 1
        
    def setPartScRat(self, x, y):
        self.partScRat[1] = (x, y)
        
    def setPart(self, x):
        for i in range(len(self.part)):
            self.part[i].value = x[i]

    def setMul(self, x):
        for i in range(len(self.amps)):
            self.amps[i].value = x[i]
            
    def setTrans(self, x):
        for i in range(len(self.trans)):
            self.trans[i].value = x[i]
            
    def setRamp(self, x):
        self.ramp.value = x
            
    def vel(self):
        return self.note['velocity']
    
    def setFmMul(self, x):
        self.fmMul.value = x
        
    def setNoiseAtt(self, x):
        self.noiseAtt.value = x
        
    def setNoiseDec(self, x):
        self.noiseDec.value = x
        
    def setNoiseSus(self, x):
        self.noiseSus.value = x
        
    def setNoiseRel(self, x):
        self.noiseRel.value = x
    
    def setNoiseMul(self, x):
        self.noiseMul.value = x
        
    def setNoiseFiltQ(self, x):
        self.noiseFiltQ.value = x

        
def bourdon():
    stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    print(bourdon)
    
def principal():
    stop1.setMul([1, 0.4, 0.3, 0.2, 0.2, 0.08, 0.04, 0.06, 0.004, 0.003, 0.003, 0.003, 0.003, 0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    print(principal)
    
def voixHumaine():
    stop1.setMul([0.3, 0.5, 0.3, 0.3, 0.7, 0.5, 0.04, 0.2, 0.04, 0.3, 0.003, 0.003, 0.003, 0.002, 0.1, 0.001, 0.001, 0, 0, 0.002])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    print(voixHumaine)
    
def cornet():
    stop1.setMul([0, 0.4, 0.3, 0.6, 0.5, 0.09, 0, 0.09, 0.004, 0.2, 0, 0.1, 0, 0.002, 0.01, 0.08, 0, 0, 0, 0.001])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    print(cornet)
    
def randPart():
    x = list(range(1, 21, 1))
    for i in range(len(partList)-1):
        x[i+1] = partList[i+1] + (((random())*2)-1)*1 
    stop1.setPart(x)
    print(randPart)

def randMul():
    stop1.setMul([random(), random()*0.5, random()*0.3, random()*0.2, random()*0.1, random()*0.05, random()*0.03, random()*0.01, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005, random()*0.005])
    print(randMul)
    
def setRamp(x):
    stop1.setRamp(x)
    
glissC = [0 for i in range(21)]

def glissUp():
    global glissC
    for i in range(len(glissC)):
        glissC[i] == 0
    if glissC[0] < 600:
        stop1.setTrans(glissC)
        for i in range(len(glissC)):
            glissC[i] = glissC[i] + 2
    else:
        for i in range(len(glissC)):
            glissC[i] = 0
    
def glissCont():
    global glissC
    for i in range(len(glissC)):
        glissC[i] == 0
    if glissC[0] < 600:
        stop1.setTrans(glissC)
        for i in range(len(glissC)):
            if i % 2 == 0:
                glissC[i] = glissC[i] + 0.4
            else:
                glissC[i] = glissC[i] + -0.4
    else:
        for i in range(len(glissC)):
            glissC[i] = 0
            
def transReset():
    global glissC
    for i in range(len(glissC)):
        glissC[i] = 0
    stop1.setTrans(glissC)

dissCount = 0
def dissocie(x):
    global dissCount
    print(x)
    if x != 0:
        dissCount += 1
        print(dissCount)
        if dissCount > 1:
            stop1.setMul([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            print("set0")
        elif dissCount == 1 :
            stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
            print("setnon0")
    if dissCount == 4:
        dissCount = 0
        
def bell():
    stop1.setFmMul(1)
    stop1.setNoiseAtt(0.001)
    stop1.setNoiseDec(0.1)
    stop1.setNoiseSus(0.01)
    stop1.setNoiseRel(0.1)    
    stop1.setNoiseMul(1)
    stop1.setNoiseFiltQ(5)
    stop1.setEnvDec([4, 5, 3, .1, .3, 0.4, .04, 0.4, .4, 0.4, .4, 0.4, .4, 0.4, .4, 0.4, .4, 0.4, .4, 0.4])
    stop1.setEnvSus([.2, .1, .2, .1, .01, 0.1, .01, 0.1, .01, 0.1, .01, 0.1, .01, 0.1, .01, 0.1, .01, 0.1, .2, 0.2])
    stop1.setEnvRel([4]*20)
    stop1.setPartScale(1.05)

partList = list(range(1, 21, 1))
transList = list(range(1, 21, 1))

i = 0

call = None

def stateChanges(address, *args):
    global i, stopV, call
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    #1e Elegie - Qui si je criais
    if i == 1:
        print('1e Elegie - Qui si je criais')
        bourdon()
        glissUpP.play()
    #2e Elegie - Tout Ange est terrible
    elif i == 2:
        print('2e Elegie - Tout Ange est terrible')
        glissUpP.stop()
        transReset()
        stop1.setEnvAtt([3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
        stop1.setEnvRel([1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    #3e Elegie - Chanter l'Amante est une chose
    elif i == 3:
        print('3e Elegie - Chanter lAmante est une chose')
        voixHumaine()
        #randMulP.play(delay=5)
        
    #4e Elegie - Vous, Arbres de la Vie
    elif i == 4:
        print('4e Elegie - Vous, Arbres de la Vie')
        randPartP.stop()
        setRamp(5)
        bourdon()
        glissCont()
    #5e Elegie - Mais les errants dis-moi
    elif i == 5:
        print('5e Elegie - Mais les errants dis-moi')
        principal()
    #6e Elegie - Figuier, depuis longtemps déjà
    elif i == 6:
        print('6e Elegie - Figuier, depuis longtemps déjà')
        voixHumaine()
    #7e Elegie - Non, plus d’imploration
    elif i == 7:
        print('7e Elegie - Non, plus d’imploration')
        randMulP.stop()
        setRamp(5)
        cornet()
    #8e Elegie - A pleins regardes, la créature
    elif i == 8:
        print('8e Elegie - A pleins regardes, la créature')
        glissUpP.stop()
        setRamp(0.02)
        randMulP.play()
    #9e Elegie - Pourquoi, s’il est loisible aussi bien
    elif i == 9:
        print('9e Elegie - Pourquoi, s’il est loisible aussi bien')
        randMulP.stop()
        glissContP.play()
    #10e Elegie - Vienne le jour enfin
    elif i == 10:
        print('10e Elegie - Vienne le jour enfin')
        glissContP.stop()
        trigDiss.setThreshold(0)

scan = OscDataReceive(port=9002, address="*", function=stateChanges)

stop1 = Stop(partList, 0, [1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01], 0.001, 0.146, 0.70, 0.1, 0.4, 10, 1, transList, 0.02, 0, 0.01, 1.5).out()

#call = CallAfter(bell, time=1)
voixHumaine()
stop1.setPartScRat(4, 1.32490)

stopV = stop1.vel()
dummy = Sig(0)
trigDiss = Thresh(stop1.vel(), threshold=100, dir=0)

randPartP = Pattern(function=randPart, time=30)
randMulP = Pattern(function=randMul, time=3)
glissUpP = Pattern(function=glissUp, time=0.08)
diss = Pattern(function=dissocie, time=0.5)
tr = TrigFunc(trigDiss, function=dissocie, arg=stop1.vel())
glissContP = Pattern(function=glissCont, time=0.1)

# Generates an audio ramp from 36 to 84, from
# which MIDI pitches will be extracted.
pitch = Phasor(freq=11, mul=48, add=36)

# Global variable to count the down and up beats.
count = 0

"""
def midi_event():
    global count
    # Retrieve the value of the pitch audio stream and convert it to an int.
    pit = int(pitch.get())

    # If the count is 0 (down beat), play a louder and longer event, otherwise
    # play a softer and shorter one.
    if count == 0:
        vel = random.randint(90, 110)
        dur = 500
    else:
        vel = random.randint(50, 70)
        dur = 125

    # Increase and wrap the count to generate a 4 beats sequence.
    count = (count + 1) % 4

    print("pitch: %d, velocity: %d, duration: %d" % (pit, vel, dur))

    # The Server's `makenote` method generates a noteon event immediately
    # and the correponding noteoff event after `duration` milliseconds.
    s.makenote(pitch=pit, velocity=vel, duration=dur)

# Generates a MIDI event every 125 milliseconds.
pat = Pattern(midi_event, 0.5).play()
"""

s.amp = 0.3

s.start()
s.gui(locals())