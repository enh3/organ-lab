import sys, time, multiprocessing
from random import uniform
from random import random
from random import randint
from pyo import *

pa_list_devices()
pm_list_devices()

VOICES_PER_CORE = 4
partList = list(range(1, 8, 1))
transList = list(range(1, 8, 1))
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25

if sys.platform.startswith("linux"):
    audio = "jack"
elif sys.platform.startswith("darwin"):
    audio = "portaudio"
else:
    print("Multicore examples don't run under Windows... Sorry!")
    exit()
    
class Stop(multiprocessing.Process):
    def __init__(self, pipe, tMul, mMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans):
        super(Stop, self).__init__()
        self.daemon = True
        self.pipe = pipe
        self.ramp = ramp
        self.inter = inter
        self.ratio = ratio
        self.index = index
        self.noiseAtt = noiseAtt
        self.noiseDec = noiseDec
        self.noiseSus = noiseSus
        self.noiseRel = noiseRel
        self.noiseMul = noiseMul
        self.noiseFiltQ = noiseFiltQ
        self.sumRat = sumRat
        self.sumTrans = sumTrans
        self.sumMul = sumMul
        self.trans = trans
        self.tMul = tMul
        self.amps = []
        self.att = []
        self.dec = []
        self.sus = []
        self.rel = []
        self.envs = []
        self.part = []
        self.snds = []
        self.mixed = []
        self.partScEnv = [(0,partScRat), (2,1)]
        self.part = part
        self.mul = mul
        self.att = att
        self.dec = dec
        self.sus = sus
        self.rel = rel
        self.rand = rand
        self.mMul = mMul

    def run(self):
        self.server = Server(audio=audio)
        self.server.deactivateMidi()
        self.server.boot().start()
        self.ramp = Sig(self.ramp)
        self.inter = Sig(self.inter)
        self.ratio = SigTo(self.ratio, self.inter)
        self.index = SigTo(self.index, self.inter)
        self.noiseAtt = self.noiseAtt
        self.noiseDec = self.noiseDec
        self.noiseSus = self.noiseSus
        self.noiseRel = self.noiseRel
        self.noiseMul = SigTo(self.noiseMul, self.inter)
        self.noiseFiltQ = SigTo(self.noiseFiltQ, self.inter)
        self.sumRat = SigTo(self.sumRat, self.inter)
        self.sumTrans = SigTo(self.sumTrans, self.inter)
        self.sumMul = SigTo(self.sumMul, self.inter)
        self.trans = SigTo(self.trans, self.inter)
        self.tMul = SigTo(self.tMul, self.inter)
        self.mid = Notein(poly=VOICES_PER_CORE, scale=1, first=0, last=127)
        self.noiseEnv = MidiAdsr(self.mid["velocity"], attack=self.noiseAtt, decay=self.noiseDec, sustain=self.noiseSus, release=self.noiseRel)
        # Handles the user polyphony independently to avoid mixed polyphony concerns (self.mid already contains 10 streams)
        for i in range(len(self.part)):
            # SigTo to avoid clicks
            self.amps.append(SigTo(self.mul[i], time=self.ramp))
            self.att.append(SigTo(self.att[i], time=self.inter))
            self.dec.append(SigTo(self.dec[i], time=self.inter))
            self.sus.append(SigTo(self.sus[i], time=self.inter))
            self.rel.append(SigTo(self.rel[i], time=self.inter))
            self.envs.append(MidiAdsr(self.mid['velocity'], attack=self.att[i], decay=self.dec[i], sustain=self.sus[i], release=self.rel[i], mul=self.amps[-1]))
            self.part.append(SigTo(self.part[i], time=0.2))
            self.snds.append(Sine(freq=(self.part[i]) * (MToF(FToM(self.mid['pitch']-0.15))) + Randi(-self.rand, self.rand, 5) + self.trans, mul=self.envs[-1]))
            self.mixed.append(self.snds[-1].mix())
        self.mix = Mix(self.mixed, 2, mul=self.mMul)
        self.filt = ButLP(self.mix, 5000)
        self.rev = STRev(self.filt, inpos=0.5, revtime=5, cutoff=4000, bal=0.15, mul=self.tMul).mix(2)
        self.sp = Spectrum(self.rev.mix(1), size=8192)
        self.rev.out()
        #self.pp = Print(self.amps, interval=2, message="Audio stream value")

        while True:
            if self.pipe.poll():
                data = self.pipe.recv()
                self.server.addMidiEvent(*data)
            time.sleep(0.001)

        self.server.stop()
        
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
        return self.mid['velocity']
    
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


if __name__ == "__main__":
    main1, child1 = multiprocessing.Pipe()
    main2, child2 = multiprocessing.Pipe()
    main3, child3 = multiprocessing.Pipe()
    main4, child4 = multiprocessing.Pipe()
    mains = [main1, main2, main3, main4]
    #blackhole_device_name = "BlackHole 16ch"
    #blackhole_output = Server(audio=blackhole_device_name).boot().start().out()
    p1 = Stop(child1, 0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 10, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT)
    p2 = Stop(child2, 0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 10, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT)
    p3 = Stop(child3, 0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 10, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT)
    p4 = Stop(child4, 0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 10, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT)
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    playing = {0: [], 1: [], 2: [], 3: []}
    currentcore = 0

    def callback(status, data1, data2):
        global currentcore
        if status == 0x80 or status == 0x90 and data2 == 0:
            for i in range(4):
                if data1 in playing[i]:
                    playing[i].remove(data1)
                    mains[i].send([status, data1, data2])
                    break
        elif status == 0x90:
            for i in range(4):
                currentcore = (currentcore + 1) % 4
                if len(playing[currentcore]) < VOICES_PER_CORE:
                    playing[currentcore].append(data1)
                    mains[currentcore].send([status, data1, data2])
                    break

    s = Server()
    s.setInputDevice(8)
    s.setOutputDevice(9)
    s.setMidiOutputDevice(98)
    s.setMidiInputDevice(99)
    s.boot()
    s.amp = 0.05
    s.start()
    raw = RawMidi(callback)
    s.gui(locals())


