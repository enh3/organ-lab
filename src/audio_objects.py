# audio_objects.py
from pyo import *
from src.pyo_server import s
from src.get_local_ip import get_local_ip
from src.stop import Stop

partList = list(range(1, 9, 1))
print(partList)
transList = list(range(1, 9, 1))
transList2 = [0] * 9
print('transList2', transList2)
openSumT = 36
closedSumT = 38
openSumR = 0.125
closedSumR = 0.25

#self, tMul, sMul, sumMul, noiseMul, part, partScRat, mul, att, dec, sus, rel, noiseAtt, noiseDec, noiseSus, noiseRel, noiseFiltQ, rand, trans, ramp, fmMul, ratio, index, inter, sumTrans, sumRat, sumInd 

ip_addr = get_local_ip()
stop1 = Stop(1, 1, 0.0001, 0.07, partList, 1, [1, 0.004, 0.012, 0, 0.0045, 0.0024, 0, 0, 0], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.08], [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.08], ([0.9]*8), [0.2, 0.3, 0.1, 0.2, 0.1, 0.07, 0.08, 0.08], 0.001, 0.146, 0.5, 0.1, 3, 0, transList2, 0.02, 0, 0.0, 0.0, 0, openSumT, openSumR, 0.3, 0.3)

