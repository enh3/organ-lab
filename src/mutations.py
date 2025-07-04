from pyo import *
from .audio_objects import stop1
from random import randint
from .emulations import * 
from random import random

print(random())

def randPart():
    x = list(range(1, 21, 1))
    for i in range(len(partList)-1):
        x[i+1] = partList[i+1] + (((random())*2)-1)*1 
    stop1.setPart(x)

def randMul():
    stop1.setMul([random(), random()*0.5, random()*0.3, random()*0.2, random()*0.1, random()*0.05, random()*0.03, random()*0.01])
    
def setRamp(x):
    stop1.setRamp(x)
    
glissC = [0 for i in range(8)]

def glissUp():
    global glissC
    #for i in range(len(glissC)):
    #    glissC[i] == 0
    #if glissC[0] < 600:
    stop1.setTrans(glissC)
    for i in range(len(glissC)):
        glissC[i] = glissC[i] + 2
    #else:
    #    for i in range(len(glissC)):
    #        glissC[i] = 0

glissUpC = None
def glissUp2():
    x = Linseg([(0,0),(90,600)])
    x.play(delay=0).graph()
    stop1.setTrans(x)
    print("gliss2")
    
glissC3 = 0
def glissUp3():
    global glissC3
    glissC3 == 0
    if glissC3 < 600:
        stop1.setTrans(glissC3)
        glissC3 = glissC3 + 0.2
    else:
        glissC3 = 0
    
def glissCont():
    global glissC
    #for i in range(len(glissC)):
    #    glissC[i] == 0
    if glissC[0] < 600:
        stop1.setTrans(glissC)
        for i in range(len(glissC)):
            if i % 2 == 0:
                glissC[i] = glissC[i] + 0.4
            else:
                glissC[i] = glissC[i] - 0.4
    else:
        for i in range(len(glissC)):
            glissC[i] = 0
    #print(glissC)
    #print("1", glissC[1])
            
def transReset():
    global glissC
    for i in range(len(glissC)):
        glissC[i] = 0
    stop1.setTrans(glissC)

dissCount = 0
def dissocie(x):
    global dissCount
    print(x)
    if x != 0:
        dissCount += 1
        print(dissCount)
        if dissCount > 1:
            stop1.setMul([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            print("set0")
        elif dissCount == 1 :
            stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
            print("setnon0")
    if dissCount == 4:
        dissCount = 0

def bellMul():
    stop1.setRamp(20)
    stop1.setMul([1, 0.01, 0.1, 0.01, 0.07, 0, 0.02, 0, 0.01, 0, 0.003, 0, 0.003, 0, 0.001, 0, 0.001, 0, 0.001, 0])
    print('bellMul')
    
def bellFM(): 
    x = Linseg([(0,0),(10,0.013864),(15,0.080007),(20,0.43982735)])
    y = Linseg([(0,1.5),(10,1.589806),(15,2.026163),(20,4)])
    x.play(delay=0)
    y.play(delay=0)
    stop1.setRatio(x)
    stop1.setIndex(y)
    print('bellFM')

def bellEnv():
    stop1.setEnvAtt([.001, .001, .001, .001, 0.001, 0.001, 0.0001, 0.0006, 0.0007, 0.0005, 0.0006, 0.0003, 0.0005, 0.0003, 0.0006, 0.0005, 0.0004, 0.0002, 0.0001, 0.0001])
    stop1.setEnvDec([1.3, .05, .02, 0, 0, 0.04, .004, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04])
    stop1.setEnvSus([.4, .1, .02, .01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .01, 0.01, .002, 0.002])
    stop1.setEnvRel([2, 0.1, 0.1, .01, .03, 0.4, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.04, .04, 0.4, .04, 0.04, .04, 0.4])
    stop1.setNoiseAtt(0.001)
    stop1.setNoiseDec(0.1)
    stop1.setNoiseSus(0.01)
    stop1.setNoiseRel(0.1)    
    stop1.setNoiseMul(0.9)
    stop1.setNoiseFiltQ(4)
    stop1.setPartScRat(1.02)
    print('bellEnv')
        
babCount = 0
def bourdonAndBell(x):
    global babCount
    #babCount = 0
    setInterpol(x)
    if babCount % 2 == 0:
        bourdon()
        babCount += 1
    elif babCount % 2 != 0:
        bell()
        babCount += 1
    print(babCount)
    
def setInterpol(x):
    stop1.setInter(x)
    
stopInterPRand = Sig(1)
def stopInter():
    global stopInterPRand
    x = randint(0, 3)
    stopInterPRand.value = randint(4, 8)
    stop1.setRamp(stopInterPRand.value)
    print(x)
    if x == 0:
        bourdon()
    elif x == 1:
        principal()
    elif x == 2:
        voixHumaine()
    elif x == 3:
        cornet()
    print('stopInter', stopInterPRand)

counter = 0

def stopInter2():
    global stopInterPRand, counter
    stopInterPRand.value = randint(4, 8)
    stop1.setRamp(stopInterPRand.value)
    if counter == 0:
        bourdon()
        counter += 1
    elif counter == 1:
        principal()
        counter += 1
    elif counter == 2:
        voixHumaine()
        counter += 1
    elif counter == 3:
        cornet()
        counter = 0
    print('stopInter', stopInterPRand)

def dynEnv():
    print('Enveloppe dynamique')
    stop1.setPart([1, 2, 3, 4, 4, 4, 0, 0])
    stop1.setMul([0.588, 0.338, 0.665, 0.773, 0.512, 0, 0, 0])
    stop1.setEnvAtt([0.285, 0.450, 0.327, 0.338, 0.385, 0.277, 0, 0])
    stop1.setEnvDec([0.02, 0.04, 0.085, 0.008, 0.008, 0.008, 0, 0])
    stop1.setEnvSus([0.446, 0.523, 0.404, 0.05, 0.05, 0.542, 0, 0])
    stop1.setEnvRel([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0, 0])
    stop1.setNoiseAtt(0.081)
    stop1.setNoiseDec(0.146)
    stop1.setNoiseSus(0.7)
    stop1.setNoiseRel(0.1)
    stop1.setNoiseMul(3)
    stop1.setNoiseFiltQ(3)
    stop1.setSumMul(0)

