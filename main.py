from pyo import *

pa_list_devices()
pm_list_devices()
s = Server()
s.setOutputDevice(1)
s.setMidiOutputDevice(98)
s.setMidiInputDevice(99)
s.boot()

from src.stop import Stop
from src.midi_sustain import NoteinSustain
from src.get_local_ip import get_local_ip
from src.ctl_gui import MyFrame
from random import random
from random import randint
import wx

partList = list(range(1, 8, 1))
transList = list(range(1, 8, 1))
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25
ip_addr = get_local_ip()

#self, tMul, sMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumRat, sumTrans

stop1 = Stop(0.8, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], ([0.9]*7), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08], 0.001, 0.146, 0.5, 0.1, 3, 0, 0, 0.02, 0, 0.0, 1.5, 0, openSumR, openSumT).out()

listTest = list(range(1, 20, 1))

autEnv = []
def automEnv(x):
    global autEnv
    for i in listTest:
        autEnv = Linseg([(0,0),(10,x[i])])
    autEnv.play()
    stop1.setEnvAtt(autEnv)


s.amp = 0.05

s.start()

path = os.path.join(os.path.expanduser("~"), "Desktop", "noise4-rev.wav")

s.recordOptions(filename=path, fileformat=0, sampletype=1)

#s.gui(locals())

app = wx.App()
frame = MyFrame(None, -1, "MIDI Control Buttons", s)
frame.Show()
app.MainLoop()

