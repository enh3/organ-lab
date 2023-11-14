import wx
from pyo import *

NCHNLS = 2

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, server):
        wx.Frame.__init__(self, parent, id, title, pos=(50, 50), size=(300, 200))
        
        self.Bind(wx.EVT_CLOSE, self.on_quit)

        # Pyo MIDI setup
        self.server = server  # Pass the Pyo server instance from organ-lab.py

        self.panel = wx.Panel(self)
        vmainsizer = wx.BoxSizer(wx.VERTICAL)
        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        leftbox = wx.BoxSizer(wx.VERTICAL)
        midbox = wx.BoxSizer(wx.VERTICAL)
        rightbox = wx.BoxSizer(wx.VERTICAL)

        sizer1 = self.createFreqSlider()
### PyoGuiControlSlider - dB scale & VuMeter ###
        sizer2 = self.createOutputBox()

        leftbox.Add(sizer1, 0, wx.ALL | wx.EXPAND, 5)


        rightbox.Add(sizer2, 1, wx.ALL | wx.EXPAND, 5)

        mainsizer.Add(leftbox, 1, wx.ALL | wx.EXPAND, 5)
        mainsizer.Add(rightbox, 0, wx.ALL | wx.EXPAND, 5)
        vmainsizer.Add(mainsizer, 1, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizerAndFit(vmainsizer)

    def on_quit(self, evt):
        self.server.stop()
        time.sleep(0.25)
        self.Destroy()

    def createFreqSlider(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self.panel, -1, "PyoGuiControlSlider: filter's center frequency (log scale)")
        sizer.Add(label, 0, wx.CENTER | wx.ALL, 5)
        self.freq = PyoGuiControlSlider(
        parent=self.panel,
            minvalue=20,
            maxvalue=20000,
            init=1000,
            pos=(0, 0),
            size=(200, 16),
            log=True,
            integer=False,
            powoftwo=False,
            orient=wx.HORIZONTAL,
        )
        # print(self.freq.getRange())
        # print(self.freq.isPowOfTwo())
        self.freq.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeFreq)
        sizer.Add(self.freq, 0, wx.ALL | wx.EXPAND, 5)
        return sizer

    def createOutputBox(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "dB slider - PyoGuiVuMeter")
        sizer.Add(label, 0, wx.CENTER | wx.ALL, 5)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        # Create the dB slider
        self.amp = PyoGuiControlSlider(
            parent=self,  # Use 'self' as the parent for the slider
            minvalue=-60,
            maxvalue=18,
            init=-12,
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
            parent=self,  # Use 'self' as the parent for the VuMeter
            nchnls=NCHNLS,
            pos=(0, 0),
            size=(5 * NCHNLS, 200),
            orient=wx.VERTICAL,
            style=0,
        )
        self.meter.setNchnls(2)

        # Register the VuMeter in the Server object.
        self.server.setMeter(self.meter)

        sizer2.Add(self.amp, 0, wx.ALL | wx.EXPAND, 5)
        sizer2.Add(self.meter, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(sizer2, 1, wx.CENTER | wx.ALL, 5)

        return sizer

    def changeFreq(self, evt):
        fr.value = evt.value

    def changeGain(self, evt):
        am.mul = pow(10, evt.value * 0.05)

