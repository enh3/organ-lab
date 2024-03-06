from pyo import *
from src.pyo_server import s

pa_list_devices()
pm_list_devices()
print('Is booted', s.getIsBooted())

from src.get_local_ip import get_local_ip
from src.stop import Stop
from src.audio_objects import stop1
stop1.out()

partList = list(range(1, 8, 1))
transList = list(range(1, 8, 1))
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25
ip_addr = get_local_ip()

#from random import random
#from random import randint
from src.midi_sustain import NoteinSustain
from src.ctl_gui import MyFrame
from src import nav
from src.nav import stateNav
from src.mutations import *
from src.patterns import *
from src.stop import *
import wx

autEnv = []
def automEnv(x):
    global autEnv
    for i in listTest:
        autEnv = Linseg([(0,0),(10,x[i])])
    autEnv.play()
    stop1.setEnvAtt(autEnv)

i = Sig(0)
vol = Sig(0)

s.amp = 0.27

#s.gui(locals())

app = wx.App()
frame = MyFrame(None, -1, "MIDI Control Buttons", s, sp)
frame.Show()
app.MainLoop()

