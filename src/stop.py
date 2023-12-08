from pyo import *
from src.pyo_server import s
from src.midi_sustain import NoteinSustain
print('Is started', s.getIsStarted())

class Stop:
    def __init__(self, tMul, mMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans):
        # scale=1 to get pitch values in hertz
        #self.note = NoteinSustain(poly=10, scale=1, first=0, last=127, channel=6)
        self.note = Notein(poly=10, scale=1, first=0, last=127, channel=6)
        self.note.keyboard()
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
        self.rev = STRev(self.filt, inpos=0.5, revtime=10, cutoff=4000, bal=0.15, mul=self.tMul).mix(2)
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
