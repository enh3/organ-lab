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

def stateNav(*args):
    global i, vol, call1, call2, call3, call4, call5  # Global index for states
    state_changed = False  # Flag to track whether a state change should be triggered
    
    # Determine if the incoming message is MIDI or OSC based on args length or type
    if len(args) == 3 and isinstance(args[0], int):
        # Handle MIDI messages
        status, data1, data2 = args
        print("MIDI:", status, data1, data2)
        if  status == 150 and data1 == 48 or status == 176 and data1 == 1 and data2 == 20: 
            i.value = 1
            state_changed = True
        elif status == 150 and data1 == 49 or status == 176 and data1 == 2 and data2 == 20:
            i.value = 2
            state_changed = True
        # Continue with similar conditions for other states...
        elif status == 182 and data1 == 20:
            vol.value = (data2 / 127) * 1.1 
            stop1.setTTMul(vol.value)

    elif len(args) == 2 and isinstance(args[0], str):
        # Handle OSC messages
        address, value = args
        print("OSC:", address, value)
        if address == "/volume":
            vol.value = value
            stop1.setTMul(abs(vol.value - 1))
        elif address == "/continue" and value == 1:
            i.value += 1  # Assuming 10 states, prevent overflow
            state_changed = True
        elif address == "/return" and value == 1:
            i.value -= 1  # Assuming starting from 1, prevent underflow
            state_changed = True

    if state_changed:
        if i.value == 1:
            stop1.setInter(0)
            glissUpP.stop()
            transReset()
            stop1.setRatio(0)
            stop1.setIndex(1)
            bourdon()
        #1e Élégie
        if i.value == 3:
            print('1e Élégie - Qui, si je criais, qui donc entendrait mon cri \nGlissandi (midi)')
            glissUpP.play()
            stop1.setTMul(0.85)
        #2e Élégie
        elif i.value == 4:
            print('2e Élégie - Toute Ange est terrible\nEnveloppe dynamique')
            glissUpP.stop()
            transReset()
            stop1.setTMul(0.55)
            dynEnv()
        #3e Élégie
        elif i.value == 6:
            print('3e Élégie - Interpolation de cloche')
            glissUpP.stop()
            transReset()
            voixHumaine()
            stop1.setTMul(0.7)
            stop1.setRatio(0)
            stop1.setIndex(1)
            stopInterP.stop()
            call2 = CallAfter(stop1.setRamp, time=2, arg=(20))
            call3 = CallAfter(bellMul, time=1)
            call4 = CallAfter(bellFM, time=1)
            call5 = CallAfter(bellEnv, time=20)
        #4e Élégie
        elif i.value == 7:
            print('4e Élégie - Verres musicaux')
            stop1.setInter(40)
            stop1.setTMul(0)
        #5e Élégie
        elif i.value == 11:
            print('5e Élégie - Mais les errants!')
            stop1.setTMul(.7)
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
            stop1.setTMul(.7)
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
        elif i.value == 19:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            stop1.setTMul(1)
            #bourdon()
            stop1.setNoiseAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
            stop1.setNoiseDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
            stop1.setEnvAtt([6, 4, 2, 2.5, 3, .4, .5, .3])
            stop1.setEnvDec([6, 4, 2, 0.3, 0.6, .4, .5, .3])
            stopP = stop1.setPart([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0])
            #stop1.noiseMul(4)
            #stopV = stop1.vel()
            #setRamp(100)
            #stop1.setInter(100)
            #call3 = CallAfter(stopInterPD, time=5)
            #setRamp(5)
            #cornet()
            #randMulP.play()
        elif i.value == 20:
            print('7e Élégie - Non, plus d\'imploration, voix maintenant mûrie, plus de clameur')
            stop1.setTMul(1)
            #bourdon()
            stop1.setNoiseAtt([3, 4, 2, 2.5, 3, .4, .5, .3])
            stop1.setNoiseDec([3, 4, 2, 0.3, 0.6, .4, .5, .3])
            stop1.setEnvAtt([6, 4, 2, 2.5, 3, .4, .5, .3])
            stop1.setEnvDec([6, 4, 2, 0.3, 0.6, .4, .5, .3])
            stopP = stop1.setPart([1, 0.01, 0.5, 0.01, 0.2, 0, 0.1, 0, 0.1, 0, 0.06, 0, 0.03, 0, 0.01, 0, 0.01, 0, 0.01, 0])
            #stop1.noiseMul(4)
            #stopV = stop1.vel()
            #setRamp(100)
            #stop1.setInter(100)
            #call3 = CallAfter(stopInterPD, time=5)
            #setRamp(5)
            #cornet()
            #randMulP.play()

midiScan = RawMidi(stateNav)
oscScan = OscDataReceive(port=9003, address="*", function=stateNav)

send = OscSend(
    input=[i, vol],
    port=8997,
    address=["counter", "volume"],
    host="127.0.0.1",
)

