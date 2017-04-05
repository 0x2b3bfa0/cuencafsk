#!/usr/bin/env python3

"""
Program to decode tresholded data from the unknown signal source in Cuenca.
GPLv2 Copyright(c) 2017 by Helio.

/

Chapuza para convertir el sonido de Cuenca en bits.
Copiar con moderación.
"""

import re
import numpy
from scipy.io import wavfile
from math import isclose


# filename = "./gqrx_20170403_122504_415311300.wav"
filename = "/Users/casa/gqrx_20170404_123132_415311300 copia.wav"
channel = 0

mark = 1300
space = 2100

frequency_tolerance = 500
amplitude_threshold = 150

rate, raw = wavfile.read(filename)
samples = numpy.array([sample[channel] for sample in raw])
crossings = numpy.where((samples[:-1] <= 0) & (samples[1:] > 0)) [0]
cycles = numpy.split(samples, crossings)

burst = []
bursts = []
for cycle in cycles:
    frequency = rate / len(cycle)
    amplitude = max([abs(x) for x in cycle])

    bit = None
    if amplitude >= amplitude_threshold:
        if numpy.isclose(frequency, space, atol=frequency_tolerance): bit = 0
        elif numpy.isclose(frequency, mark, atol=frequency_tolerance): bit = 1
    burst += [(bit, len(cycle), frequency)]

    if bit is None and burst != []:
        bursts += [burst]
        burst = []

tuples = sum(bursts, [])
signal = sum([[(x[0]*500 if x[0] is not None else 0) + 2500] * x[1] for x in tuples], [])
# signal = sum([[(x[0]*500 if x[0] is not None else 0) + 2500] * (x[1]-1) + [0] for x in tuples], [])
frequencies = sum([[x[2]+2100] * x[1] for x in tuples], [])

import matplotlib.pyplot as plt
plt.plot(range(len(frequencies)),frequencies)
plt.plot(range(len(signal)), signal)
plt.plot(range(len(raw)), raw)
plt.plot(range(len(raw)), [1300+2100]*len(raw))
plt.plot(range(len(raw)), [2100+2100]*len(raw))
plt.show()

# for burst in bursts:
#     burst = ''.join([str(x[0]) for x in burst])
#     match = re.search(r'^(1{10,250})(.+)(1{10,150})$', burst)
#     try: print(match.group(2))
#     except: pass
#     # print(i)
#     # try:
#     #     print("{PREAMBLE: {}; DATA {}; ENDING: {};}".format(match.group(1), match.group(2), match.group(3)))
#     # except:
#     #     pass
