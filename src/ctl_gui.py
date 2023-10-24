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
        vmainsizer = wx.BoxSizer(wx.HORIZONTAL)

        ### PyoGuiControlSlider - dB scale & VuMeter ###
        sizer2 = self.createOutputBox()
        vmainsizer.Add(sizer2, 0, wx.LEFT | wx.ALL, 5)
        
        self.panel.SetSizerAndFit(vmainsizer)

    def on_quit(self, evt):
        self.server.stop()
        time.sleep(0.25)
        self.Destroy()

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

    def changeFreq(self, evt):
        fr.value = evt.value

    def changeGain(self, evt):
        self.server.amp = pow(10, evt.value * 0.05)

