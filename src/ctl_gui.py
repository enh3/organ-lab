import wx
from pyo import *
from src.pyo_server import s
#from . import nav
#from .nav import stateNav

NCHNLS = 2

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, server):
        wx.Frame.__init__(self, parent, id, title, pos=(50, 50), size=(600, 600))
        
        self.Bind(wx.EVT_CLOSE, self.on_quit)

        # Pyo MIDI setup
        self.server = server  # Pass the Pyo server instance from organ-lab.py

        self.panel = wx.Panel(self)
        vmainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)
        self.count = -1

        ### PyoGuiControlSlider - dB scale & VuMeter ###
        sizer1 = self.createOutputBox()
        sizer2 = self.createMidiButtons(self.count)

        keyboard = PyoGuiKeyboard(self.panel)
        keyboard.Bind(EVT_PYO_GUI_KEYBOARD, self.onMidiNote)

        vmainsizer.Add(sizer1, 0, wx.LEFT | wx.ALL, 5)
        vmainsizer.Add(sizer2, 1, wx.LEFT | wx.ALL, 5)
        vmainsizer.Add(keyboard, 2, wx.LEFT | wx.ALL, 5)
        
        self.panel.SetSizerAndFit(vmainsizer)

    def on_quit(self, evt):
        self.server.stop()
        time.sleep(0.25)
        self.Destroy()

    def onMidiNote(self, evt):
        self.server.addMidiEvent(status=144, data1=evt.value[0], data2=evt.value[1])
        print("Pitch:    %d" % evt.value[0])
        print("Velocity: %d" % evt.value[1])

    def createOutputBox(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, -1, "dB slider - PyoGuiVuMeter")
        sizer.Add(label, 0, wx.CENTER | wx.ALL, 5)
        
        sliders_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create the dB slider
        self.amp = PyoGuiControlSlider(
            parent=self.panel,  # Use 'self.panel' as the parent for the slider
            minvalue=-60,
            maxvalue=18,
            init=-20,
            pos=(0, 0),
            size=(200, 16),
            log=False,
            integer=False,
            powoftwo=False,
            orient=wx.VERTICAL,
        )
        self.amp.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeGain)

        # Create the VuMeter
        self.meter = PyoGuiVuMeter(
            parent=self.panel,  # Use 'self.panel' as the parent for the VuMeter
            nchnls=NCHNLS,
            pos=(0, 0),
            size=(5 * NCHNLS, 200),
            orient=wx.VERTICAL,
            style=0,
        )
        self.meter.setNchnls(2)

        # Register the VuMeter in the Server object.
        self.server.setMeter(self.meter)

        sliders_sizer.Add(self.amp, 0, wx.ALL | wx.EXPAND, 5)
        sliders_sizer.Add(self.meter, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(sliders_sizer, 0, wx.CENTER | wx.ALL, 5)

        return sizer

    def createMidiButtons(self, event):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, -1, "Navigation")
        sizer.Add(label, 0, wx.CENTER | wx.ALL, 5)
        
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        increase_button = wx.Button(self.panel, label="Continue", pos=(10, 10))
        increase_button.Bind(wx.EVT_BUTTON, self.on_increase)

        decrease_button = wx.Button(self.panel, label="Return", pos=(10, 10))
        decrease_button.Bind(wx.EVT_BUTTON, self.on_decrease)

        buttons_sizer.Add(decrease_button, 0, wx.ALL | wx.EXPAND, 5)
        buttons_sizer.Add(increase_button, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(buttons_sizer, 0, wx.CENTER | wx.ALL, 5)
        return sizer

    def changeGain(self, evt):
        self.server.amp = pow(10, evt.value * 0.05)

    def on_increase(self, evt):
        self.count += 1
        print(self.count)
        #self.server.addMidiEvent(status=176, data1=self.count, data2=20)
        stateNav(176, self.count, 20, "midi")

    def on_decrease(self, evt):
        self.count -= 1
        print(self.count)
        #self.server.addMidiEvent(status=176, data1=self.count, data2=20)
        stateNav(176, self.count, 20, "midi")

