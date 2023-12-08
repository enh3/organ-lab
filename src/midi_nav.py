from pyo import *
from src.pyo_server import s
from .emulations import *
from .mutations import *
from .patterns import *
from .audio_objects import stop1

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
val = 0

def midiNav(ctl, chan):
    global i, stopV, call1, call2, mScan, s
    if chan == 6:
        #1e Élégie
        if ctl == 1 and m1Value.get() == 20: 
            print('1e Élégie - Qui, si je criais, qui donc entendrait mon cri \nGlissandi (midi)')
            glissUpP.play()
        #2e Élégie
        elif ctl == 2 and m2Value.get() == 20:
            print('2e Élégie - Toute Ange est terrible\nEnveloppe dynamique')
            glissUpP.stop()
            transReset()
            dynEnv()
        #3 Élégie
        elif ctl == 3 and m3Value.get() == 20:
            print('3e Élégie - Interpolation de cloche')
            voixHumaine()
            glissUpP.stop()
            transReset()
            setInterpol(0.05)
            stop1.setRamp(0.05)
            stop1.setRatio(0)
            stop1.setIndex(1)
            stopInterP.stop()
            setInterpol(900000)
            stop1.setRamp(900000)
            call2 = CallAfter(bell, time=5)
        #4e Élégie
        elif ctl == 4 and m4Value.get() == 20:
            print('4e Élégie - Verres musicaux')
            stop1.setTMul(0)
        #5e Élégie
        elif ctl == 5 and m5Value.get() == 20:
            print('5e Élégie - Figuier, depuis longtemps déjà ce m\'est un signe')
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
        elif ctl == 7 and m7Value.get() == 20:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            print('chan: ', chan, 'ctl: ', ctl, 'val: ', m7Value.get())
            randMulP.stop()
            setRamp(5)
            cornet()
        #8e Élégie
        elif ctl == 8 and m8Value.get() == 20:
            print('8e Elegie - A pleins regardes, la créature')
            randMulP.stop()
            setRamp(5)
            cornet()
        #9 
        elif ctl == 9 and m9Value.get() == 20:
            print('9e Elegie - Pourquoi, s\’il est loisible aussi bien')
            glissUpP.stop()
            setRamp(0.02)
            randMulP.play()
        #10 
        elif ctl == 10 and m10Value.get() == 20:
            print('10e Élégie - Vienne le jour enfin, sortant de la voyance encolérée')
            randMulP.stop()
            glissContP.play()
        elif ctl == 11 and m11Value.get() == 20:
            randMulP.start()
        elif ctl == 12 and m12Value.get() == 20:    
            print('Dissocié')
            randMulP.stop()
            bourdon()
            dissP.play()

mScan = CtlScan2(midiNav, toprint=False)
