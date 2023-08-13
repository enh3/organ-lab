from pyo import *

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(98)
s.setMidiInputDevice(0)
s.boot()

mCtl = [0]
mValue = Midictl(ctlnumber=mCtl, minscale=0, maxscale=127, channel=6)

def mStateChanges(ctl, chan):
    global i, stopV, call1, call2, mValue, mCtl
    mCtl[1] = ctl
    print(mCtl[1])
    mValue = Midictl(ctlnumber=mCtl, minscale=0, maxscale=127, channel=6)
    pp = Print(mValue, method=1, message="Audio stream value")
    print(int(mValue.get()))

mScan = CtlScan2(mStateChanges, toprint=False)

s.amp = 0.05

s.start()

path = os.path.join(os.path.expanduser("~"), "Desktop", "noise4-rev.wav")

s.recordOptions(filename=path, fileformat=0, sampletype=1)

s.gui(locals())
