from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
from random import random
from random import randint

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(2)
#s.setMidiOutputDevice(5)
#s.setMidiInputDevice(0)
s.boot()

partList = list(range(1, 8, 1))
transList = list(range(1, 8, 1))
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25

path = "/Users/kjel/Documents/Ableton/Enregistrement_dorgue Project/Fichiers" + "2023-03-07_brdn_pres_avecBruit_chr_mono.wav"

#sf = SfPlayer("/Users/kjel/Documents/Ableton/Élegies Project/2023-05-17_looped_env_dyn_norm.wav", speed=[1, 1], loop=True, mul=1).mix(1).out()

#sf = SfPlayer("/Users/kjel/Documents/Ableton/Élegies Project/Audio/Bruit_de_soufflerie/2023-03-06_bruit_de_souf_loin.wav", speed=1, loop=True, mul=0.05).mix(2).out()

#sfSpec = Spectrum(sf.mix(1), size=8192)

class Stop:
    def __init__(self, tMul, mMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans):
        # scale=1 to get pitch values in hertz
        #self.note = NoteinSustain(poly=10, scale=1, first=0, last=127, channel=0)
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
        self.sumRat = SigTo(sumRat, self.inter)
        self.sumTrans = SigTo(sumTrans, self.inter)
        self.sumMul = SigTo(sumMul, self.inter)
        self.trans = SigTo(trans, self.inter)
        self.tMul = SigTo(tMul, self.inter)
        self.amps = []
        self.att = []
        self.dec = []
        self.sus = []
        self.rel = []
        self.envs = []
        self.part = []
        self.snds = []
        self.mixed = []
        self.velocity = [Clip(Sig(v), max=0.01, mul=100) for v in self.note['velocity']]
        self.partScEnv = [(0,partScRat), (2,1)]
        self.partSc = MidiLinseg(self.velocity, self.partScEnv)
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=noiseAtt, decay=noiseDec, sustain=noiseSus, release=noiseRel)
        self.noise = PinkNoise(1.5) * self.noiseEnv
        self.n1Harm = Resonx(self.noise, freq=(self.note['pitch']), q=1, mul=0.5)
        self.n3Harm = Resonx(self.noise, freq=(self.note['pitch']*(22/8)), q=8, mul=1)
        self.n5Harm = Resonx(self.noise, freq=(self.note['pitch']*(8/3)), q=3, mul=0.5)
        self.n10Harm = Resonx(self.noise, freq=(self.note['pitch']*(16/3)), q=3, mul=0.1)
        self.nMix = Mix(self.n1Harm+self.n3Harm+self.n5Harm+self.n10Harm, 1, mul=self.noiseMul)
        self.wind = PinkNoise(0.001) * self.noiseEnv
        self.windF = Tone(self.wind, 950)
        self.fmod = self.note['pitch'] * self.ratio
        self.amod = self.fmod * self.index
        self.mod = Sine(self.fmod, mul=self.amod)
        #self.harmT = HarmTable([0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
        #self.harmOsc = Osc(table=self.harmT, freq=10**self.partSc) * (MToF(FToM(self.note['pitch'])-0.15)) + Randi(-rand, rand, 5) + self.trans[-1] + self.mod
        self.sum = SumOsc(freq=(MToF(FToM(self.note['pitch'])-0.15+self.sumTrans) + self.trans), ratio=self.sumRat, index=0.3, mul=self.noiseEnv*self.sumMul)
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.note already contains 10 streams)
        for i in range(len(part)):
            # SigTo to avoid clicks
            self.amps.append(SigTo(mul[i], time=self.ramp))
            self.att.append(SigTo(att[i], time=self.inter))
            self.dec.append(SigTo(dec[i], time=self.inter))
            self.sus.append(SigTo(sus[i], time=self.inter))
            self.rel.append(SigTo(rel[i], time=self.inter))
            self.envs.append(MidiAdsr(self.note['velocity'], attack=att[i], decay=dec[i], sustain=sus[i], release=rel[i], mul=self.amps[-1]))
            #self.trans.append(SigTo(trans, time=0.025))
            self.part.append(SigTo(part[i], time=0.2))
            self.snds.append(Sine(freq=(self.part[i]**self.partSc) * (MToF(FToM(self.note['pitch']-0.15))) + Randi(-rand, rand, 5) + self.trans + self.mod, mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=mMul)
        self.filt = ButLP(self.mix + self.nMix + self.sum + self.windF, 5000)
        self.rev = STRev(self.filt, inpos=0.5, revtime=5, cutoff=4000, bal=0.15, mul=self.tMul).mix(2)
        self.sp = Spectrum(self.rev.mix(1), size=8192)
        #self.pp = Print(self.att, interval=2, message="Audio stream value")
        
    def out(self):
        self.rev.out()
        return self
        
    def setTMul(self, x):
        self.tMul.value = x
        
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
        self.trans.value = x
            
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

#self, tMul, sMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans

stop1 = Stop(0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 10, 1, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT).out()

def bourdon():
    stop1.setMul([1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0])
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
    
glissC = [0 for i in range(8)]

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

glissUpC = None
def glissUp2():
    x = Linseg([(0,0),(90,600)])
    x.play(delay=0).graph()
    stop1.setTrans(x)
    print("gliss2")
    
glissC3 = 0
def glissUp3():
    global glissC3
    glissC3 == 0
    if glissC3 < 600:
        stop1.setTrans(glissC3)
        glissC3 = glissC3 + 0.2
    else:
        glissC3 = 0
    
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
    bellCall1 = CallAfter(stop1.setEnvAtt, time=60, arg=(.001, .001, .001, .001, 0.001, 0.001, 0.0001, 0.0006, 0.0007, 0.0005, 0.0006, 0.0003, 0.0005, 0.0003, 0.0006, 0.0005, 0.0004, 0.0002, 0.0001, 0.0001)).play()
    bellCall2 = CallAfter(stop1.setEnvDec, time=60, arg=(1.3, .05, .02, 0, 0, 0.04, .004, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04)).play()
    bellCall3 = CallAfter(stop1.setEnvSus, time=60, arg=(.4, .1, .02, .01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .002, 0.002)).play()
    bellCall4 = CallAfter(stop1.setEnvRel, time=60, arg=(2, 0.1, 0.1, .01, .03, 0.4, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.4, .04, 0.04, .04, 0.4)).play()
    stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    stop1.setRatio(0.43982735)
    stop1.setIndex(4)
    stop1.setNoiseAtt(0.001)
    stop1.setNoiseDec(0.1)
    stop1.setNoiseSus(0.01)
    stop1.setNoiseRel(0.1)    
    stop1.setNoiseMul(0.9)
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
    
stopInterPRand = Sig(1)
def stopInter():
    global stopInterPRand
    x = randint(0, 3)
    stopInterPRand.value = randint(1, 10)
    print(x)
    if x == 0:
        bourdon()
    elif x == 1:
        principal()
    elif x == 2:
        voixHumaine()
    elif x == 3:
        cornet()
    print('stopInter', stopInterPRand)

i = 0

call1 = None
call2 = None

def stateChanges(address, *args):
    global i, stopV, call1, call2
    print(address)
    print(args)
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    #1e Élégie
    if i == 2:
        print('Glissandi')
        glissUpP.play()
    #2e Élégie
    elif i == 3:
        print('Enveloppe dynamique')
        glissUpP.stop()
        transReset()
        stop1.setMul([0.588, 0.062, 0.412, 0.61, 0.092, 0.092, 0.6, 0])
        #principal()
        stop1.setEnvAtt([0.181, 0.169, 0.073, 0.073, 0.088, 0.088, 0.1, 0.2])
        stop1.setEnvDec([0.02, 0.04, 0.01, 0.008, 0.008, 0.008, 0.008, 0.008])
        stop1.setEnvSus([0.6, 0.5, 0.7, 0.2, 0.5, 0.09, 0.05, 0.5])
        stop1.setEnvRel([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        stop1.setNoiseAtt(0.2)
    #3 Élégie
    elif i == 4:
        print('Interpolation de cloche')
        stopInterP.stop()
        voixHumaine()
        setInterpol(60)
        stop1.setRamp(60)
        call2 = CallAfter(bell, time=5)
    #4e Élégie
    elif i == 5:
        print('Tmul = 0')
        stop1.setTMul(0)
    #5e Élégie
    elif i == 7:
        print('Interpolation de jeux')
        stop1.setTMul(1)
        glissUpP.stop()
        transReset()
        stop1.setRatio(0)
        stop1.setIndex(1)
        bourdon()
        stop1.setRamp(5)
        stopInterP.play()
    #6e Élégie 
    #7e Élégie
    elif i == 10:
        print('7e Elegie - Non, plus d’imploration')
        randMulP.stop()
        setRamp(5)
        cornet()
    #8e Élégie
    elif i == 11:
        print('7e Elegie - Non, plus d’imploration')
        randMulP.stop()
        setRamp(5)
        cornet()
    #9 
    elif i == 12:
        print('8e Elegie - A pleins regardes, la créature')
        glissUpP.stop()
        setRamp(0.02)
        randMulP.play()
    #10 
    elif i == 13:
        print('9e Elegie - Pourquoi, s’il est loisible aussi bien')
        randMulP.stop()
        glissContP.play()
    elif i == 14:
        randMulP.start()
    elif i == 15:    
        print('Dissocié')
        randMulP.stop()
        bourdon()
        dissP.play()
        
scan = OscDataReceive(port=7400, address="*", function=stateChanges)

'''
stop1.setMul([1, 0.5, 0.412, 0.61, 0.092, 0.092, 0.6, 0])
#principal()
stop1.setEnvAtt([0.181, 0.169, 0.073, 0.073, 0.088, 0.088, 0.1, 0.2])
stop1.setEnvDec([0.02, 0.04, 0.01, 0.008, 0.008, 0.008, 0.008, 0.008])
stop1.setEnvSus([1, 0.4, 0.6, 0.35, 0.5, 0.25, 0.04, 0.5])
stop1.setEnvRel([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
stop1.setNoiseAtt(0.2)
'''

listTest = list(range(1, 20, 1))

autEnv = []
def automEnv(x):
    global autEnv
    for i in listTest:
        autEnv = Linseg([(0,0),(10,x[i])])
    autEnv.play()
    stop1.setEnvAtt(autEnv)


principal()
stopP = stop1.setPart([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0])
stop1.setNoiseAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
stop1.setNoiseDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
stop1.setEnvAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
stop1.setEnvDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
stopV = stop1.vel()


dummy = Sig(0)
trigDiss = Thresh(stop1.vel(), threshold=100, dir=0)

randPartP = Pattern(function=randPart, time=30)
randMulP = Pattern(function=randMul, time=3)
glissUpP = Pattern(function=glissUp, time=0.12)
glissUpP3 = Pattern(function=glissUp3, time=1)
dissP = Pattern(function=dissocie, time=0.5)
babP = Pattern(function=bourdonAndBell, time=0.2, arg=0.2)
tr = TrigFunc(trigDiss, function=dissocie, arg=stop1.vel())
glissContP = Pattern(function=glissCont, time=0.1)
stopInterP = Pattern(function=stopInter, time=Sig(stopInterPRand))

#glissUpP.play()
#glissUp2()
#glissUpP3.play()
#bourdon()

# Generates an audio ramp from 36 to 84, from
# which MIDI pitches will be extracted.
pitch = Phasor(freq=11, mul=48, add=36)

# Global variable to count the down and up beats.
count = 0

s.amp = 0.05

s.start()

path = os.path.join(os.path.expanduser("~"), "Desktop", "noise4-rev.wav")

s.recordOptions(filename=path, fileformat=0, sampletype=1)

s.gui(locals())
