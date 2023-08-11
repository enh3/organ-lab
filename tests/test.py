from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
from random import random
from random import randint

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(98)
s.setMidiInputDevice(0)
s.boot()

def mStateChanges(ctrl, chan):
    global i, stopV, call1, call2, mValue, pp, mCtrl, mChan
    mValue.setCtlNumber(ctrl)
    mValue.setChannel(chan)
    print(int(mValue.get()))
    if chan == 6 and int(mValue.get()) == 20:
        #1e Élégie
        if ctrl == 1: 
            print('Glissandi') 
        #2e Élégie
        elif ctrl == 2:
            print('Enveloppe dynamique')

mValue = Midictl(1, minscale=0, maxscale=127, channel=1)
mScan = CtlScan2(mStateChanges, toprint=False)

s.amp = 0.05

s.start()

s.gui(locals())