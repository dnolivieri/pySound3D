#!/usr/bin/env python

import sys
import pylab
import matplotlib.pyplot as plt
import numpy as np


f=open('vdata.txt','r')

time = []
xdat = []
ydat = []
for eachLine in f:
    line = [float(x) for x in eachLine.split()]
    time.append(line[0])
    xdat.append(line[1])
    ydat.append(line[2])
f.close()

plt.specgram(ydat)
    
plt.show()
