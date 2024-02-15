from pyo import *
from src.pyo_server import s
from .emulations import *
from .mutations import *
from .patterns import *
from .audio_objects import stop1

def midiNav(status, data1, data2):
    global i, s
    if status == 150 or status == 176:
        #1e Élégie
        if  status == 150 and data1 == 48 or status == 176 and data1 == 1 and data2 ==20: 
            print('1e Élégie - Qui, si je criais, qui donc entendrait mon cri \nGlissandi (midi)')
            glissUpP.play()
        #2e Élégie
        elif status == 150 and data1 == 49 or status == 176 and data1 == 2 and data2 ==20:
            print('2e Élégie - Toute Ange est terrible\nEnveloppe dynamique')
            glissUpP.stop()
            transReset()
            dynEnv()
        #3 Élégie
        elif status == 150 and data1 == 50 or status == 176 and data1 == 3 and data2 ==20:
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
        elif status == 150 and data1 == 51 or status == 176 and data1 == 4 and data2 ==20:
            print('4e Élégie - Verres musicaux')
            stop1.setTMul(0)
        #5e Élégie
        elif status == 150 and data1 == 52 or status == 176 and data1 == 5 and data2 ==20:
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
        elif status == 150 and data1 == 53 or status == 176 and data1 == 6 and data2 ==20:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            print('chan: ', chan, 'ctl: ', ctl, 'val: ', m7Value.get())
            randMulP.stop()
            setRamp(5)
            cornet()
        #8e Élégie
        elif status == 150 and data1 == 54 or status == 176 and data1 == 7 and data2 ==20:
            print('8e Elegie - A pleins regardes, la créature')
            randMulP.stop()
            setRamp(5)
            cornet()
        #9 
        elif status == 150 and data1 == 55 or status == 176 and data1 == 8 and data2 ==20:
            print('9e Elegie - Pourquoi, s\’il est loisible aussi bien')
            glissUpP.stop()
            setRamp(0.02)
            randMulP.play()
        #10 
        elif status == 150 and data1 == 56 or status == 176 and data1 == 9 and data2 ==20:
            print('10e Élégie - Vienne le jour enfin, sortant de la voyance encolérée')
            randMulP.stop()
            glissContP.play()
        elif status == 150 and data1 == 57 or status == 176 and data1 == 10 and data2 ==20:
            randMulP.start()
        elif status == 150 and data1 == 58 or status == 176 and data1 == 11 and data2 ==20:    
            print('Dissocié')
            randMulP.stop()
            bourdon()
            dissP.play()

midi = RawMidi(midiNav)
