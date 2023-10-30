from pyo import *

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
    global i, stopV, call1, call2
    #print('m2Value: ', m2Value.get())
    if chan == 6:
        #1e Élégie
        if ctl == 1 and m1Value.get() == 20 or val == 20: 
            print('Glissandi')
            print('chan: ', chan)
            print('ctl: ', ctl)
            print('m1Value: ', m1Value.get() or val == 20)
            glissUpP.play()
        #2e Élégie
        elif ctl == 2 and m2Value.get() == 20 or val == 20:
            print('Enveloppe dynamique')
            print('chan: ', chan)
            print('ctl: ', ctl)
            print('m2Value: ', m2Value.get())
            glissUpP.stop()
            transReset()
            dynEnv()
        #3 Élégie
        elif ctl == 3 and m3Value.get() == 20 or val == 20:
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

mScan = CtlScan2(midiNav, toprint=False)

