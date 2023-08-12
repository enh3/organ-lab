from pyo import *

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(98)
s.setMidiInputDevice(0)
s.boot()

m = Midictl(ctlnumber=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minscale=0, maxscale=127, channel=0)
pp = Print(m, method=1, message="Audio stream value")

def mStateChanges(ctl, chan):
    global m
    m.setCtlNumber(ctl) 
    #print('chan: ', chan)
    #print('ctl: ', ctl)
    #print('val: ', int(m.get()))
    if chan == 6 and val == 20:   
        #1e Élégie
        if ctl == 1: 
            print('Glissandi') 
        #2e Élégie
        elif ctl == 2:
            print('Enveloppe dynamique')

mScan = CtlScan2(mStateChanges, toprint=False)

s.amp = 0.05

s.start()

s.gui(locals())