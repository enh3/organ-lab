from pyo import *
from midi_sustain import NoteinSustain
from random import random
from random import randint
from get_local_ip import get_local_ip
import wx
from ctl_gui import MyFrame

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(98)
s.setMidiInputDevice(99)
s.boot()

partList = list(range(1, 8, 1))
transList = list(range(1, 8, 1))
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25
ip_addr = get_local_ip()

class Stop:
    def __init__(self, tMul, mMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans):
        # scale=1 to get pitch values in hertz
        self.note = NoteinSustain(poly=10, scale=1, first=0, last=127, channel=0)
        #self.note = Notein(poly=10, scale=1, first=0, last=127, channel=0)
        #self.note.keyboard()
        self.partScRat = Sig(partScRat)
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
        self.n1Harm = Resonx(self.noise, freq=(self.note['pitch']), q=self.noiseFiltQ, mul=0.5)
        self.n3Harm = Resonx(self.noise, freq=(self.note['pitch']*(22/8)), q=self.noiseFiltQ, mul=1)
        self.n5Harm = Resonx(self.noise, freq=(self.note['pitch']*(8/3)), q=self.noiseFiltQ, mul=0.5)
        self.n10Harm = Resonx(self.noise, freq=(self.note['pitch']*(16/3)), q=self.noiseFiltQ, mul=0.1)
        self.nMix = Mix(self.n1Harm+self.n3Harm+self.n5Harm+self.n10Harm, 1, mul=self.noiseMul)
        self.wind = PinkNoise(0.001) * self.noiseEnv
        self.windF = Tone(self.wind, 950)
        self.fmod = self.note['pitch'] * self.ratio
        self.amod = self.fmod * self.index
        self.mod = Sine(self.fmod, mul=self.amod)
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
            self.part.append(SigTo(part[i], time=0.2))
            self.snds.append(Sine(freq=(self.part[i]**self.partSc) * (MToF(FToM(self.note['pitch']-0.15))) + Randi(-rand, rand, 5) + self.trans + self.mod, mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=mMul)
        self.filt = ButLP(self.mix + self.nMix + self.sum + self.windF, 5000)
        self.rev = STRev(self.filt, inpos=0.5, revtime=5, cutoff=4000, bal=0.15, mul=self.tMul).mix(2)
        self.sp = Spectrum(self.rev.mix(1), size=8192)
        #self.pp = Print(self.amps, interval=2, message="Audio stream value")
        
    def out(self):
        self.rev.out()
        return self
        
    def setTMul(self, x):
        self.tMul.value = x

    def setSumMul(self, x):
        self.sumMul.value = x
        
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

stop1 = Stop(0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 3, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT).out()

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
    bellCall1 = CallAfter(stop1.setEnvAtt, time=120, arg=(.001, .001, .001, .001, 0.001, 0.001, 0.0001, 0.0006, 0.0007, 0.0005, 0.0006, 0.0003, 0.0005, 0.0003, 0.0006, 0.0005, 0.0004, 0.0002, 0.0001, 0.0001)).play()
    bellCall2 = CallAfter(stop1.setEnvDec, time=120, arg=(1.3, .05, .02, 0, 0, 0.04, .004, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04)).play()
    bellCall3 = CallAfter(stop1.setEnvSus, time=120, arg=(.4, .1, .02, .01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .002, 0.002)).play()
    bellCall4 = CallAfter(stop1.setEnvRel, time=120, arg=(2, 0.1, 0.1, .01, .03, 0.4, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.4, .04, 0.04, .04, 0.4)).play()
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

def dynEnv():
    print('Enveloppe dynamique')
    stop1.setPart([1, 2, 3, 4, 4, 4, 0, 0])
    stop1.setMul([0.588, 0.338, 0.665, 0.773, 0.512, 0, 0, 0])
    stop1.setEnvAtt([0.285, 0.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
    stop1.setEnvDec([0.02, 0.04, 0.085, 0.008, 0.008, 0.008, 0, 0])
    stop1.setEnvSus([0.446, 0.523, 0.404, 0.05, 0.05, 0.542, 0, 0])
    stop1.setEnvRel([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0])
    stop1.setNoiseAtt(0.081)
    stop1.setNoiseDec(0.146)
    stop1.setNoiseSus(0.7)
    stop1.setNoiseRel(0.1)
    stop1.setNoiseMul(3)
    stop1.setNoiseFiltQ(3)
    stop1.setSumMul(0)

i = Sig(0)
vol = Sig(1)

call1 = None
call2 = None

def stateChanges(address, *args):
    global i, vol, stopV, call1, call2
    print(address)
    print(args)
    print('i = ', i.value)
    if address == "/volume":
        vol.value = args[0]
        stop1.setTMul(vol.value)
    if address == "/continue" and args[0] == 1:
        i.value += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i.value -= 1
        print(i)
    #1e Élégie
    if i.value == 2:
        print('Glissandi')
        glissUpP.play()
    #2e Élégie
    elif i.value == 3:
        print('Enveloppe dynamique')
        glissUpP.stop()
        transReset()
        dynEnv()
    #3 Élégie
    elif i.value == 4:
        print('Interpolation de cloche')
        stopInterP.stop()
        voixHumaine()
        setInterpol(60)
        stop1.setRamp(60)
        call2 = CallAfter(bell, time=5)
    #4e Élégie
    elif i.value == 5:
        print('Tmul = 0')
        stop1.setTMul(0)
    #5e Élégie
    elif i.value == 7:
        print('Interpolation de jeux')
        #reset()
        setInterpol(0)
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
    elif i.value == 10:
        print('8e Elegie')
        stop1.setTMul(0)
    #8e Élégie
    elif i.value == 10:
        print('8e Elegie')
        stop1.setTMul(1)
        stopInterP.stop()
        randMulP.stop()
        setRamp(5)
        bourdon()
    #9e Élégie
    elif i.value == 11:
        print('9e Elegie')
        randMulP.stop()
        setRamp(5)
        bourdon()
    #9 
    #10 
    elif i.value == 13:
        print('10e Elegie')
        glissUpP.stop()
        setRamp(0.02)
        randMulP.play()
        #reset()
        stop1.setTMul(1)
        glissUpP.stop()
        transReset()
        stop1.setRatio(0)
        stop1.setIndex(1)
        bourdon()
        stop1.setRamp(10)
        stopInterP.play()
    elif i.value == 14:
        randMulP.start()
    elif i.value == 15:    
        print('Dissocié')
        randMulP.stop()
        bourdon()
        dissP.play()

#print_i = Print(i, interval=2, message="Audio stream value")
print("IP ADDRESS", ip_addr)
scan = OscDataReceive(port=9003, address="*", function=stateChanges)

send = OscSend(
    input=[i, vol],
    port=8996,
    address=["counter", "volume"],
    host="192.168.100.143",
)

#send.setBufferRate(175)
m1Value = Midictl(ctlnumber=1, minscale=0, maxscale=127, channel=6)
m2Value = Midictl(ctlnumber=2, minscale=0, maxscale=127, channel=6)
m3Value = Midictl(ctlnumber=3, minscale=0, maxscale=127, channel=6)
m4Value = Midictl(ctlnumber=4, minscale=0, maxscale=127, channel=6)
m5Value = Midictl(ctlnumber=5, minscale=0, maxscale=127, channel=6)
m6Value = Midictl(ctlnumber=6, minscale=0, maxscale=127, channel=6)
m7Value = Midictl(ctlnumber=7, minscale=0, maxscale=127, channel=6)
m8Value = Midictl(ctlnumber=8, minscale=0, maxscale=127, channel=6)
m9Value = Midictl(ctlnumber=9, minscale=0, maxscale=127, channel=6)
m10Value = Midictl(ctlnumber=10, minscale=0, maxscale=127, channel=6)
#pp = Print(mValue, method=0, interval=0.25, message="Audio stream value")

def mStateChanges(ctl, chan):
    global i, stopV, call1, call2
    #print('m2Value: ', m2Value.get())
    if chan == 6:
        #1e Élégie
        if ctl == 1 and m1Value.get() == 20: 
            print('Glissandi')
            print('chan: ', chan)
            print('ctl: ', ctl)
            print('m1Value: ', m1Value.get())
            glissUpP.play()
        #2e Élégie
        elif ctl == 2 and m2Value.get() == 20:
            print('Enveloppe dynamique')
            print('chan: ', chan)
            print('ctl: ', ctl)
            print('m2Value: ', m2Value.get())
            glissUpP.stop()
            transReset()
            dynEnv()
        #3 Élégie
        elif ctl == 3 and m3Value.get() == 20:
            print('Interpolation de cloche')
            glissUpP.stop()
            transReset()
            stop1.setRatio(0)
            stop1.setIndex(1)
            stopInterP.stop()
            voixHumaine()
            setInterpol(120)
            stop1.setRamp(120)
            call2 = CallAfter(bell, time=5)
        #4e Élégie
        elif ctl == 4 and m4Value.get() == 20:
            print('Tmul = 0')
            stop1.setTMul(0)
        #5e Élégie
        elif ctl == 5 and m5Value.get() == 20:
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
        elif ctl == 6 and m7Value.get() == 20:
            print('5e Elegie')
            randMulP.stop()
            setRamp(5)
            cornet()
        #8e Élégie
        elif ctl == 7 and m8Value.get() == 20:
            print('7e Elegie - Non, plus d’imploration')
            randMulP.stop()
            setRamp(5)
            cornet()
        #9 
        elif ctl == 8 and m9Value.get() == 20:
            print('8e Elegie - A pleins regardes, la créature')
            glissUpP.stop()
            setRamp(0.02)
            randMulP.play()
        #10 
        elif ctl == 9 and m10Value.get() == 20:
            print('9e Elegie - Pourquoi, s’il est loisible aussi bien')
            randMulP.stop()
            glissContP.play()
        elif ctl == 10 and m11Value.get() == 20:
            randMulP.start()
        elif ctl == 11 and m12Value.get() == 20:    
            print('Dissocié')
            randMulP.stop()
            bourdon()
            dissP.play()

mScan = CtlScan2(mStateChanges, toprint=False)


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

'''
principal()
stopP = stop1.setPart([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0])
stop1.setNoiseAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
stop1.setNoiseDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
stop1.setEnvAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
stop1.setEnvDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
stopV = stop1.vel()
'''

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

#s.gui(locals())

app = wx.App()
frame = MyFrame(None, -1, "MIDI Control Buttons", s)
frame.Show()
app.MainLoop()

