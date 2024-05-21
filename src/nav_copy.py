from pyo import *
from src.pyo_server import s
from .emulations import *
from .mutations import *
from .patterns import *
from .audio_objects import stop1

call1 = None
call2 = None
call3 = None
call4 = None
call5 = None

i = Sig(0)
vol = Sig(1)

def stateNav(source, *args):
    global i, vol, call1, call2, call3, call4, call5  # Global index for states
    state_changed = False  # Flag to track whether a state change should be triggered

    # Determine the state index based on the source
    if source == "midi":
        status, data1, data2 = args
        if  status == 150 and data1 == 48 or status == 176 and data1 == 1 and data2 ==20: 
            i.value = 1
            state_changed = True
        elif status == 150 and data1 == 49 or status == 176 and data1 == 2 and data2 ==20:
            i.value = 2
            state_changed = True
        elif status == 150 and data1 == 50 or status == 176 and data1 == 3 and data2 ==20:
            i.value = 3
            state_changed = True
        elif status == 150 and data1 == 51 or status == 176 and data1 == 4 and data2 ==20:
            i.value = 4
            state_changed = True
        elif status == 150 and data1 == 52 or status == 176 and data1 == 5 and data2 ==20:
            i.value = 5
            state_changed = True
        elif status == 150 and data1 == 53 or status == 176 and data1 == 6 and data2 ==20:
            i.value = 6
            state_changed = True
        elif status == 150 and data1 == 54 or status == 176 and data1 == 7 and data2 ==20:
            i.value = 7
            state_changed = True
        elif status == 150 and data1 == 55 or status == 176 and data1 == 8 and data2 ==20:
            i.value = 8
            state_changed = True
        elif status == 150 and data1 == 56 or status == 176 and data1 == 9 and data2 ==20:
            i.value = 9
            state_changed = True
        elif status == 150 and data1 == 57 or status == 176 and data1 == 10 and data2 ==20:
            i.value = 10
            state_changed = True
        elif status == 150 and data1 == 58 or status == 176 and data1 == 11 and data2 ==20:    
            i.value = 11
            state_changed = True
        elif status == 150 and data1 == 59 or status == 176 and data1 == 12 and data2 ==20:    
            i.value = 12
            state_changed = True
        elif status == 150 and data1 == 60 or status == 176 and data1 == 13 and data2 ==20:    
            i.value = 13
            state_changed = True
        elif status == 150 and data1 == 61 or status == 176 and data1 == 14 and data2 ==20:    
            i.value = 14
            state_changed = True
        elif status == 150 and data1 == 62 or status == 176 and data1 == 15 and data2 ==20:    
            i.value = 15
            state_changed = True
        elif status == 150 and data1 == 63 or status == 176 and data1 == 16 and data2 ==20:    
            i.value = 16
            state_changed = True
        elif status == 150 and data1 == 64 or status == 176 and data1 == 17 and data2 ==20:    
            i.value = 17
            state_changed = True
        elif status == 150 and data1 == 65 or status == 176 and data1 == 18 and data2 ==20:    
            i.value = 18
            state_changed = True
        elif status == 150 and data1 == 66 or status == 176 and data1 == 19 and data2 ==20:    
            i.value = 19
            state_changed = True
        elif status == 150 and data1 == 67 or status == 176 and data1 == 20 and data2 ==20:    
            i.value = 20 
            state_changed = True
        elif status == 182 and data1 == 20:
            vol.value = data2/127 
            stop1.setTTMul(vol.value) 

    elif source == "osc":
        address, value = args
        # OSC directly modifies 'i', or you could map addresses to indexes as well
        if address == "/volume":
            vol.value = value
            stop1.setTMul(abs(vol.value-1))
        if address == "/continue" and value == 1:
            i.value += 1 # Assuming 10 states, prevent overflow
            state_changed = True
        elif address == "/return" and value == 1:
            i.value -= 1 # Assuming starting from 1, prevent underflow
            state_changed = True

    if state_changed:
        #1e Élégie
        if i.value == 3:
            print('1e Élégie - Qui, si je criais, qui donc entendrait mon cri \nGlissandi (midi)')
            glissUpP.play()
        #2e Élégie
        elif i.value == 4:
            print('2e Élégie - Toute Ange est terrible\nEnveloppe dynamique')
            glissUpP.stop()
            transReset()
            dynEnv()
        #3e Élégie
        elif i.value == 6:
            print('3e Élégie - Interpolation de cloche')
            glissUpP.stop()
            transReset()
            voixHumaine()
            stop1.setTMul(.9)
            stop1.setRatio(0)
            stop1.setIndex(1)
            stopInterP.stop()
            call2 = CallAfter(stop1.setRamp, time=2, arg=(240))
            call3 = CallAfter(bellMul, time=1)
            call4 = CallAfter(bellFM, time=1)
            call5 = CallAfter(bellEnv, time=120)
        #4e Élégie
        elif i.value == 7:
            print('4e Élégie - Verres musicaux')
            stop1.setInter(40)
            stop1.setTMul(0)
        #5e Élégie
        elif i.value == 11:
            print('5e Élégie - Mais les errants!')
            stop1.setTMul(1)
            stop1.setInter(0)
            glissUpP.stop()
            transReset()
            stop1.setRatio(0)
            stop1.setIndex(1)
            bourdon()
            stop1.setEnvAtt([2.285, 2.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
            #setRamp(100)
            #stop1.setInter(100)
            call3 = CallAfter(stopInterPD, time=5)
        elif i.value == 12:
            print('5e Élégie - Mais les errants!')
            stop1.setTMul(1)
            glissUpP.stop()
            transReset()
            stop1.setRatio(0)
            stop1.setIndex(1)
            bourdon()
            stop1.setEnvAtt([2.285, 2.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
            #setRamp(100)
            #stop1.setInter(100)
            call3 = CallAfter(stopInterPD, time=5)
        #6e Élégie
        #7e Élégie
        elif i.value == 14:
            print('8e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            stop1.setTMul(0)
        elif i.value == 18:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            stop1.setTMul(1)
            bourdon()
            stop1.setEnvAtt([2.285, 2.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
            #setRamp(100)
            #stop1.setInter(100)
            call3 = CallAfter(stopInterPD, time=5)
            #setRamp(5)
            #cornet()
            randMulP.play()

# Wrapper or partial functions to specify the source type
from functools import partial
midi_nav = partial(stateNav, "midi")
osc_nav = partial(stateNav, "osc")

midiScan = RawMidi(midi_nav)
oscScan = OscDataReceive(port=9003, address="*", function=osc_nav)

send = OscSend(
    input=[i, vol],
    port=8997,
    address=["counter", "volume"],
    host="127.0.0.1",
)

