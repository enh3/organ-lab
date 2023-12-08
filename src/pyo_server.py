from pyo import *

# Create Pyo server
s = Server()
s.setOutputDevice(1)
s.setMidiInputDevice(99)
s.setMidiOutputDevice(4)
s.boot()
s.start()
