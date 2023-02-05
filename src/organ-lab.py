from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
from random import random
from random import randint

pa_list_devices()
#pm_list_devices()
s = Server()
s.setOutputDevice(1)
#s.setMidiOutputDevice(1)
s.setMidiInputDevice(99)
s.boot()

partList = list(range(1, 21, 1))
transList = list(range(1, 21, 1))

class Stop:
    def __init__(self, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseMul, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter):
        # scale=1 to get pitch values in hertz
        self.note = Notein(poly=10, scale=1, first=0, last=127, channel=0)
        self.note.keyboard()
        #self.partScRat = Sig(partScRat)
        self.ramp = Sig(ramp)
        self.inter = Sig(inter)
        self.ratio = SigTo(ratio, self.inter)
        self.index = SigTo(index, self.inter)
        self.noiseAtt = SigTo(noiseAtt, self.inter)
        self.noiseDec = SigTo(noiseDec, self.inter)
        self.noiseSus = SigTo(noiseSus, self.inter)
        self.noiseRel = SigTo(noiseRel, self.inter)
        self.noiseMul = SigTo(noiseMul, self.inter)
        self.noiseFiltQ = SigTo(noiseFiltQ, self.inter)
        self.amps = []
        self.att = []
        self.dec = []
        self.sus = []
        self.rel = []
        self.envs = []
        self.part = []
        self.snds = []
        self.mixed = []
        self.trans = []
        self.velocity = [Clip(Sig(v), max=0.01, mul=100) for v in self.note['velocity']]
        self.partScEnv = [(0,partScRat), (2,1)]
        self.partSc = MidiLinseg(self.velocity, self.partScEnv)
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=noiseAtt, decay=noiseDec, sustain=noiseSus, release=noiseRel)
        self.noise = PinkNoise(1.5) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.note['pitch']*(20/4)), q=self.noiseFiltQ)
        self.noise = Mix(self.noise, 1, mul=self.noiseMul)
        self.fmod = self.note['pitch'] * self.ratio
        self.amod = self.fmod * self.index
        self.mod = Sine(self.fmod, mul=self.amod)
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # SigTo to avoid clicks
            self.amps.append(SigTo(mul[i], time=self.ramp))
            self.att.append(SigTo(att[i], time=self.inter))
            self.dec.append(SigTo(dec[i], time=self.inter))
            self.sus.append(SigTo(sus[i], time=self.inter))
            self.rel.append(SigTo(rel[i], time=self.inter))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=dec[i], sustain=sus[i], release=rel[i], mul=self.amps[-1]))
            self.trans.append(SigTo(trans[i], time=0.025))
            self.part.append(SigTo(part[i], time=0.2))
            self.snds.append(Sine(freq=(self.part[i]**self.partSc) * (MToF(FToM(self.note['pitch'])-0.4)) + Randi(-rand, rand, 5) + self.trans[-1] + self.mod, mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=1)
        self.filt = ButLP(self.mix+self.noise, 20000)
        self.rev = STRev(self.filt, inpos=0.5, revtime=5, cutoff=4000, bal=0.15).mix(2)
        self.sp = Spectrum(self.rev, 8192)
        #self.pp = Print(self.att, interval=2, message="Audio stream value")
        
        
    def out(self):
        self.rev.out()
        return self
        
    def setInter(self, x):
        self.inter.value = x
        
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
            
    def setMul(self, x):
        for i in range(len(self.amps)):
            self.amps[i].value = x[i]
        
    def setPartScRat(self, x):
        self.partScEnv[0] = (0, x)
        
    def setPart(self, x):
        for i in range(len(self.part)):
            self.part[i].value = x[i]
            
    def setTrans(self, x):
        for i in range(len(self.trans)):
            self.trans[i].value = x[i]
            
    def setRamp(self, x):
        self.ramp.value = x
            
    def vel(self):
        return self.note['velocity']
    
    def setFmMul(self, x):
        self.fmMul.value = x
        
    def setRatio(self, x):
        self.ratio.value = x
        
    def setIndex(self, x):
        self.index.value = x
        
    def setNoiseAtt(self, x):
        self.noiseEnv.setAttack(x)
        
    def setNoiseDec(self, x):
        self.noiseEnv.setDecay(x)
        
    def setNoiseSus(self, x):
        self.noiseEnv.setSustain(x)
        
    def setNoiseRel(self, x):
        self.noiseEnv.setRelease(x)
    
    def setNoiseMul(self, x):
        self.noiseEnv.setMul(x)
        
    def setNoiseFiltQ(self, x):
        self.noiseFiltQ.value = x


stop1 = Stop(partList, 1, [1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01], ([0.9]*20), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01], 0.001, 0.146, 0.70, 0.1, 0.4, 10, 1, transList, 0.02, 0, 0.0, 1.5, 0).out()

def bourdon():
    stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvDec([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvSus([0.9]*20)
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setRatio(0)
    stop1.setIndex(1)
    stop1.setNoiseAtt(0.001)
    stop1.setNoiseDec(0.146)
    stop1.setNoiseSus(0.70)
    stop1.setNoiseRel(0.1)    
    stop1.setNoiseMul(4)
    stop1.setNoiseFiltQ(10)
    #stop1.setPartSc(1.05)
    stop1.setPartScRat(1)
    print(bourdon)
    
def principal():
    stop1.setMul([1, 0.4, 0.3, 0.2, 0.2, 0.08, 0.04, 0.06, 0.004, 0.003, 0.003, 0.003, 0.003, 0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001])
    stop1.setEnvAtt([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvRel([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    print(principal)
    
def voixHumaine():
    stop1.setMul([0.3, 0.9, 0.9, 0.9, 0.7, 0.9, 0.9, 0.01, 0.04, 0.3, 0.003, 0.003, 0.003, 0.002, 0.1, 0.001, 0.001, 0, 0, 0.002])
    stop1.setEnvAtt([0.2, 0.3, 0.2, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvDec([0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
    stop1.setEnvSus([1]*20)
    stop1.setEnvRel([0.5, 0.3, 0.6, 0.2, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
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
    print("0", glissC[0])
    print("1", glissC[1])
            
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
        
bellCall1 = None
bellCall2 = None
bellCall3 = None
bellCall4 = None

def bell():
    global bellCall1, bellCall2, bellCall3, bellCall4 
    bellCall1 = CallAfter(stop1.setEnvAtt, time=15, arg=(.001, .001, .001, .001, 0.001, 0.001, 0.0001, 0.0006, 0.0007, 0.0005, 0.0006, 0.0003, 0.0005, 0.0003, 0.0006, 0.0005, 0.0004, 0.0002, 0.0001, 0.0001)).play()
    bellCall2 = CallAfter(stop1.setEnvDec, time=15, arg=(1.3, .05, .02, 0, 0, 0.04, .004, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04)).play()
    bellCall3 = CallAfter(stop1.setEnvSus, time=15, arg=(.4, .1, .02, .01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .002, 0.002)).play()
    bellCall4 = CallAfter(stop1.setEnvRel, time=15, arg=(2, 0.1, 0.1, .01, .03, 0.4, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.4, .04, 0.04, .04, 0.4)).play()
    stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    stop1.setRatio(0.43982735)
    stop1.setIndex(4)
    stop1.setNoiseAtt(0.001)
    stop1.setNoiseDec(0.1)
    stop1.setNoiseSus(0.01)
    stop1.setNoiseRel(0.1)    
    stop1.setNoiseMul(0.5)
    stop1.setNoiseFiltQ(4)
    #stop1.setPartSc(1.05)
    stop1.setPartScRat(1.02)
    print(bell)
    
babCount = 0
def bourdonAndBell(x):
    global babCount
    #babCount = 0
    setInterpol(x)
    if babCount % 2 == 0:
        bourdon()
        babCount += 1
    elif babCount % 2 != 0:
        bell()
        babCount += 1
    print(babCount)
    
def setInterpol(x):
    stop1.setInter(x)
    
def autom3():
    x = Linseg([(0,0),(80,0.01)])
    y = Linseg([(0,0),(80,5)])
    x.play(delay=0).graph()
    y.play(delay=0).graph()
    stop1.setRatio(x)
    stop1.setIndex(y)
    
def stopInter():
    x = randint(0, 3)
    print(x)
    if x == 0:
        bourdon()
    elif x == 1:
        principal()
    elif x == 2:
        voixHumaine()
    elif x == 3:
        cornet()

i = 0

call = None
call2 = None

def stateChanges(address, *args):
    global i, stopV, call, call2
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    #1 Bourdon
    if i == 1:
        bourdon()
    #2 Principal
    elif i == 2:
        principal()
    #3 Voix
    elif i == 3:
        voixHumaine()
    #4 Cornet
    elif i == 4:
        principal()
        glissContP.play()
    #5 Gliss
    elif i == 5:
        print('Glissandi')
        bourdon()
        glissUpP.play()
    #6 Stop interp
    elif i == 6:
        print('Interpolation de jeux')
        glissUpP.stop()
        transReset()
        stop1.setRatio(0)
        stop1.setIndex(1)
        bourdon()
        stop1.setRamp(5)
        stopInterP.play()
    #7 Bell interp
    elif i == 7:
        print('Interpolation de cloche')
        stopInterP.stop()
        voixHumaine()
        setInterpol(15)
        stop1.setRamp(15)
        call2 = CallAfter(bell, time=5)
    #8 Enveloppe
    elif i == 8:
        print('Enveloppe dynamique')
        glissUpP.stop()
        principal()
        stop1.setEnvAtt([3, 2, 1, 2, 3, 2, 1, 2, 3, 2, 1, 4, 2, 1, 4, 2, 5, 3, 6, 2])
        stop1.setEnvRel([1, 2, 3, 2, 1, 2, 3, 2, 1, 2, 3, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
        stop1.setNoiseAtt(4)
    #9 Aléatoire
    elif i == 9:
        print('Aléatoire')
        randMulP.start()
    #10 Dissocié
    elif i == 10:
        print('Dissocié')
        randMulP.stop()
        bourdon()
        dissP.play()
    #10e Elegie - Vienne le jour enfin
    elif i == 11:
        print('7e Elegie - Non, plus d’imploration')
        randMulP.stop()
        setRamp(5)
        cornet()
    #10e Elegie - Vienne le jour enfin
    elif i == 12:
        print('7e Elegie - Non, plus d’imploration')
        randMulP.stop()
        setRamp(5)
        cornet()
    #10e Elegie - Vienne le jour enfin
    elif i == 13:
        print('8e Elegie - A pleins regardes, la créature')
        glissUpP.stop()
        setRamp(0.02)
        randMulP.play()
    #10e Elegie - Vienne le jour enfin
    elif i == 14:
        print('9e Elegie - Pourquoi, s’il est loisible aussi bien')
        randMulP.stop()
        glissContP.play()
        

scan = OscDataReceive(port=9002, address="*", function=stateChanges)

#voixHumaine()
#setInterpol(100)
#stop1.setRamp(100)
#call1 = CallAfter(bourdon, time=4)
#autom()
#call1 = CallAfter(setInterpol, time=90, arg=60)
#call2 = CallAfter(stop1.setRamp, time=90, arg=60)
#call3 = CallAfter(bell, time=100)
#bell()
#randPartP.play()
#call1 = CallAfter(stop1.setEnvAtt, time=4, arg=(.1, .1, .1, .1, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01))

#call3 = CallAfter(stop1.setEnvAtt, time=4, arg=(5, .1, .1, .1, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01))

listTest = list(range(1, 20, 1))

autEnv = []
def automEnv(x):
    global autEnv
    for i in listTest:
        autEnv = Linseg([(0,0),(10,x[i])])
    autEnv.play()
    stop1.setEnvAtt(autEnv)

#stop1.setEnvAtt([0.1, .1, .1, .1, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])
#automEnv([20, .1, .1, .1, 0.1, 0.07, 0.08, 0.6, 0.07, 0.05, 0.06, 0.03, 0.05, 0.03, 0.06, 0.05, 0.04, 0.02, 0.01, 0.01])


stopV = stop1.vel()
dummy = Sig(0)
trigDiss = Thresh(stop1.vel(), threshold=100, dir=0)

randPartP = Pattern(function=randPart, time=30)
randMulP = Pattern(function=randMul, time=3)
glissUpP = Pattern(function=glissUp, time=0.08)
dissP = Pattern(function=dissocie, time=0.5)
babP = Pattern(function=bourdonAndBell, time=0.2, arg=0.2)
tr = TrigFunc(trigDiss, function=dissocie, arg=stop1.vel())
glissContP = Pattern(function=glissCont, time=0.1)
stopInterP = Pattern(function=stopInter, time=randint(5, 10))

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

path = os.path.join(os.path.expanduser("~"), "Desktop", "pretty2.wav")
# Record for 10 seconds a 24-bit wav file.
s.recordOptions(filename=path, fileformat=0, sampletype=1)

s.gui(locals())