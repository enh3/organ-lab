from pyo import *
from src.pyo_server import s
from .emulations import *
from .mutations import *
from .patterns import *
from .audio_objects import stop1

i = 0
def stateNav(source, *args):
    global i  # Global index for states
    print(i)
    state_changed = False  # Flag to track whether a state change should be triggered

    # Determine the state index based on the source
    if source == "midi":
        status, data1, data2 = args
        if  status == 150 and data1 == 48 or status == 176 and data1 == 1 and data2 ==20: 
            i = 1
            state_changed = True
        elif status == 150 and data1 == 49 or status == 176 and data1 == 2 and data2 ==20:
            i = 2
            state_changed = True
        elif status == 150 and data1 == 50 or status == 176 and data1 == 3 and data2 ==20:
            i = 3
            state_changed = True
        elif status == 150 and data1 == 51 or status == 176 and data1 == 4 and data2 ==20:
            i = 4
            state_changed = True
        elif status == 150 and data1 == 52 or status == 176 and data1 == 5 and data2 ==20:
            i = 5
            state_changed = True
        elif status == 150 and data1 == 53 or status == 176 and data1 == 6 and data2 ==20:
            i = 6
            state_changed = True
        elif status == 150 and data1 == 54 or status == 176 and data1 == 7 and data2 ==20:
            i = 7
            state_changed = True
        elif status == 150 and data1 == 55 or status == 176 and data1 == 8 and data2 ==20:
            i = 8
            state_changed = True
        elif status == 150 and data1 == 56 or status == 176 and data1 == 9 and data2 ==20:
            i = 9
            state_changed = True
        elif status == 150 and data1 == 57 or status == 176 and data1 == 10 and data2 ==20:
            i = 10
            state_changed = True
        elif status == 150 and data1 == 58 or status == 176 and data1 == 11 and data2 ==20:    
            i = 11
            state_changed = True

    elif source == "osc":
        address, value = args
        # OSC directly modifies 'i', or you could map addresses to indexes as well
        if address == "/continue" and value == 1:
            i = min(i + 1, 11)  # Assuming 10 states, prevent overflow
            state_changed = True
        elif address == "/return" and value == 1:
            i = max(i - 1, 1)  # Assuming starting from 1, prevent underflow
            state_changed = True

    if state_changed:
        #1e Élégie
        if i == 1:
            print('1e Élégie - Qui, si je criais, qui donc entendrait mon cri \nGlissandi (midi)')
            glissUpP.play()
        #2e Élégie
        elif i == 2:
            print('2e Élégie - Toute Ange est terrible\nEnveloppe dynamique')
            glissUpP.stop()
            transReset()
            dynEnv()
        #3e Élégie
        elif i == 3:
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
        elif i == 4:
            print('4e Élégie - Verres musicaux')
            stop1.setTMul(0)
        #5e Élégie
        elif i == 5:
            print('5e Élégie - Figuier, depuis longtemps déjà ce m\'est un signe')
            stop1.setTMul(1)
            glissUpP.stop()
            transReset()
            stop1.setRatio(0)
            stop1.setIndex(1)
            bourdon()
            stop1.setEnvAtt([2.285, 2.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
            stop1.setRamp(5)
            call3 = CallAfter(stopInterPD, time=5)
        #6e Élégie
        #7e Élégie
        elif i == 6:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            print('chan: ', chan, 'ctl: ', ctl, 'val: ', m7Value.get())
            randMulP.stop()
            setRamp(5)
            cornet()
        #8e Élégie
        elif i == 7:
            print('8e Elegie - A pleins regardes, la créature')
            randMulP.stop()
            setRamp(5)
            cornet()
        #9 
        elif i == 8:
            print('9e Elegie - Pourquoi, s\’il est loisible aussi bien')
            glissUpP.stop()
            setRamp(0.02)
            randMulP.play()
        #10 
        elif i == 9:
            print('10e Élégie - Vienne le jour enfin, sortant de la voyance encolérée')
            randMulP.stop()
            glissContP.play()
        elif i == 10:
            randMulP.start()
        elif i == 11:
            print('Dissocié')
            randMulP.stop()
            bourdon()
            dissP.play()

# Wrapper or partial functions to specify the source type
from functools import partial
midi_nav = partial(stateNav, "midi")
osc_nav = partial(stateNav, "osc")

midiScan = RawMidi(midi_nav)
oscScan = OscDataReceive(port=9003, address="*", function=osc_nav)
