from pyo import *
from src.pyo_server import s
from src.midi_sustain import NoteinSustain
print('Is started', s.getIsStarted())

#sp = Spectrum(Sig(0.2))

class Stop:
    def __init__(self, tMul, mMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumTrans, sumRat, sumInd, tTMul):
        global sp
        # scale=1 to get pitch values in hertz
        self.note = NoteinSustain(poly=10, scale=1, first=0, last=127, channel=1)
        #self.note = Notein(poly=10, scale=1, first=0, last=127)
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
        self.sumInd = Sig(sumInd)
        self.sumTrans = SigTo(sumTrans, self.inter)
        self.sumMul = SigTo(sumMul, self.inter)
        self.trans = []
        self.tMul = SigTo(tMul, self.inter)
        self.tTMul = Sig(tTMul)
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
            self.snds.append(Sine(freq=(self.part[i]**self.partSc) * (MToF(FToM(self.note['pitch'])-.15)) + Randi(-rand, rand, 5) + self.trans[-1] + self.mod, mul=self.envs[-1]))
            self.sum = SumOsc(freq=(MToF(FToM(self.note['pitch'])-0.+self.sumTrans) + self.trans[-1]), ratio=self.sumRat, index=self.sumInd, mul=self.noiseEnv*self.sumMul)
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=mMul)
        self.filt = ButLP(self.mix + self.nMix + self.sum + self.windF, 5000)
        self.comp = Compress(self.filt, thresh=-15, ratio=6, mul=self.tMul*self.tTMul)
        self.rev = STRev(self.comp, inpos=0.5, revtime=10, cutoff=4000, bal=0.15, mul=self.tMul).mix(2)
        sp = Spectrum(self.rev.mix(1), size=8192)
        #self.p = Print(self.trans, interval=2, message="Trans")
        #self.pp = Print(self.tMul, interval=.1, message="tMul")
        #self.tfon = TrigFunc(self.note["trigon"], function=self.noteon, arg=list(range(10)))
        #self.tfoff = TrigFunc(self.note["trigoff"], function=self.noteoff, arg=list(range(10)))
        
    def out(self):
        self.rev.out()
        return self
        
    def setTMul(self, x):
        self.tMul.value = x
        print("tMul: ", self.tMul.value)

    def setTTMul(self, x):
        self.tTMul.value = x
        print("tTTMul: ", self.tTMul.value)

    def setSumMul(self, x):
        self.sumMul.value = x
        
    def setSumRat(self, x):
        self.sumRat.value = x

    def setSumInd(self, x):
        self.sumInd.value = x

    def setInter(self, x):
        self.inter.value = x
        print('inter', self.inter.value)
        
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
            print(self.part)
            
    def setTrans(self, x):
        for i in range(len(self.trans)):
            self.trans[i].value = x[i]
            #print(self.trans[i].value)
            
    def setRamp(self, x):
        self.ramp.value = x
        print('ramp', self.ramp.value)
            
    def vel(self):
        return self.note['velocity']
    
    def setFmMul(self, x):
        self.fmMul.value = x
        
    def setRatio(self, x):
        self.ratio.value = x
        print("ratio", self.ratio.value)
        
    def setIndex(self, x):
        self.index.value = x
        print("index", self.index.value)
        
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

    def noteon(self, voice):
        "Print pitch and velocity for noteon event."
        pit = int(self.note["pitch"].get(all=True)[voice])
        vel = int(self.note["velocity"].get(all=True)[voice] * 127)
        print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

    def noteoff(self, voice):
        "Print pitch and velocity for noteoff event."
        pit = int(self.note["pitch"].get(all=True)[voice])
        vel = int(self.note["velocity"].get(all=True)[voice] * 127)
        print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))
