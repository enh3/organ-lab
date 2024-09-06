from pyo import *

# Create Pyo server
s = Server(buffersize=512)
s.setOutputDevice(4)
s.setMidiInputDevice(99)
#s.setMidiOutputDevice(4)
s.boot()
s.start()
