from pyo import *

s = Server()
s.setMidiInputDevice(99)
s.boot()

note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
note.keyboard()

p1Env = MidiAdsr(note['velocity'], attack=0.1, decay=0.02, sustain=0.3, release=0.1, mul=1)

freq = MToF(note['pitch'])

p1 = Sine(freq=freq, mul=p1Env)

sound = Mix(p1, 1)

SL = sound.out()
SR = sound.out(1)

s.amp = 0.3

s.start()
s.gui(locals())
