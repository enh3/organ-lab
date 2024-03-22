import sys, time, multiprocessing
from pyo import *

if sys.platform.startswith("linux"):
    audio = "jack"
elif sys.platform.startswith("darwin"):
    audio = "portaudio"
else:
    print("Multicore examples don't run under Windows... Sorry!")
    exit()

# Create Pyo server
s = Server(buffersize=512)
s.setOutputDevice(1)
s.setMidiInputDevice(99)
#s.setMidiOutputDevice(4)
s.boot()
s.start()
