trigDiss = Thresh(stop1.vel(), threshold=100, dir=0)

randPartP = Pattern(function=randPart, time=30)
randMulP = Pattern(function=randMul, time=3)
glissUpP = Pattern(function=glissUp, time=0.12)
glissUpP3 = Pattern(function=glissUp3, time=1)
dissP = Pattern(function=dissocie, time=0.5)
babP = Pattern(function=bourdonAndBell, time=0.2, arg=0.2)
tr = TrigFunc(trigDiss, function=dissocie, arg=stop1.vel())
glissContP = Pattern(function=glissCont, time=0.1)
stopInterP = Pattern(function=stopInter, time=Sig(stopInterPRand))

