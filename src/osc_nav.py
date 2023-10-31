from pyo import *
from src.get_local_ip import get_local_ip

i = Sig(0)
vol = Sig(1)

call1 = None
call2 = None

def oscNav(address, *args):
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
#print("IP ADDRESS", ip_addr)
scan = OscDataReceive(port=9003, address="*", function=oscNav)

send = OscSend(
    input=[i, vol],
    port=8996,
    address=["counter", "volume"],
    host="192.168.100.143",
)

