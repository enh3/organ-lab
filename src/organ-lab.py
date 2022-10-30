from pyo import *
from s047_midi_sustain_and_polyphony import NoteinSustain
import keyboard

s = Server()
s.setMidiInputDevice(99)
s.boot()

class Stop :
    def __init__(self, part, mul, att, rel, rand):
        self.note = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)
        self.note.keyboard()
        self.partials = part
        self.muls = mul
        self.attacks = att
        self.releases = rel
        self.rand = rand
        self.randObj = Randi(self.rand, self.rand, 5)
        self.mulsObj = Sig(self.muls)
        self.freq = MToF(self.note['pitch'])
        self.pitch = [(partial * self.freq) for partial in self.partials]
        self.noiseEnv = MidiAdsr(self.note['velocity'], attack=0.001, decay=0.146, sustain=0.70, release=0.1)
        self.noise = PinkNoise(0.7) * self.noiseEnv
        self.noise = Reson(self.noise, freq=(self.freq*(20/4)), q=10, mul=.4)
        self.noise = Mix(self.noise, 1)
        self.sound = [Sine(freq=pit+rand, mul=amp*MidiAdsr(self.note['velocity'], attack=attacks, decay=0, sustain=1, release=releases)) for pit, rand, amp, attacks, releases in zip(self.pitch, self.randObj, self.mulsObj, self.attacks, self.releases)]
        self.sound = Mix(self.sound, 1)
        self.mix = STRev(self.sound+self.noise, inpos=0.5, revtime=5, cutoff=4000, bal=0.15)
    def out(self):
        #"Sends the synth's signal to the audio output and return the object itself."
        self.mix.out()
        return self
    def setMuls(self, x):
        self.mulsObj.value = x
        print(self.muls)
        print(self.mulsObj.value)
    def setRand(self, x):
        self.rand = x
        self.randObj.min = -x
        self.randObj.max = x
        print(self.rand)
        print(self.randObj.min)
        print(self.randObj.max)
        
def rand():
    bourdon.setRand(100)
    
def bourdonToPrincipal():
    bourdon.setMuls([0, 0, 0, 0, 0, 0, 0.1, 0.5, 0.1, 0.4, 0.06, 0.3, 0.03, 0.3, 0.01, 0.3, 0.01, 0.2, 0.01, 0.2])
    
pat2 = Pattern(function=bourdonToPrincipal, time=1).play()

partList = list(range(1, 21, 1))

bourdon = Stop(partList, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], [.1, .4]).out()

#a = bourdon.setRand(100)

#note = NoteinSustain(scale=0)






   
 
'''
def dissoc():
    
def softAtk():

'''

i = 0
currentFunc = 0

def stateChanges(address, *args):
    global i
    if address == "/continue" and args[0] == 1:
        i += 1
        print(i)
    elif address == "/return" and args[0] == 1:
        i -= 1
        print(i)
    if i == 1:
        bourdonToPrincipal()
    elif i == 2:
        rand()
    elif i == 3:
        softAtk()


#if rec["/continue"] == 1 :
   # print("hello")
    #env.play()
    
#pat = Pattern(function=printM, time=3).play()
scan = OscDataReceive(port=9002, address="*", function=stateChanges)
    
#pat1 = Pattern(function=bourdonToPrincipal, time=1).play()


'''
def trans():
    transV.value = Adsr(attack=240, release=10, mul=1000).play()

transEnv = Pattern(trans, 120).play()
'''
#Fader se comporte pas comme attendu avec le méthode .range, donnant 0.5 à 1 pour .range(0, 1) par example
'''  
def bToD():
    p1Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(1, 0.635).play()#.635
    p2Mul.value = Fader(fadein=2, fadeout=2, dur=4, mul=1, add=0).range(0.2, 0.823).play()#.723
    p3Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(0.3, 0.515).play()#.515
    p4Mul.value = Fader(fadein=2, fadeout=2, dur=4).range(0.01, 0.535).play()#.535


bourdToDiap = Pattern(bToD, 4).play()
'''
#pp = Print(transV, interval=0.1, message="Audio stream value")

s.amp = 0.3

s.start()
s.gui(locals())