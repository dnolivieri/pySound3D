#!/usr/bin/env python
"""
    dnolivieri:
      - discrete transform based upon experimental 
        IIR measurements.
"""

import numpy as np
import scipy.io
import scipy.signal
import scipy.fftpack
from scikits.audiolab import Sndfile, Format
import matplotlib.pyplot as plt

import time
import bisect
import os, fnmatch
import glob
import sys
import re

import itertools
import json

class HRIRTransform:
    def __init__(self, S, soundFile):
        self.S = S        
        self.inputSound, self.sampleRate = self.get_input_signal(soundFile)

    def get_input_signal(self, soundFile):
        f = Sndfile( soundFile, 'r')
        fs = f.samplerate
        nc = f.channels
        enc = f.encoding
        nf= f.nframes
        data = f.read_frames(nf)
        #data_float = f.read_frames(1000, dtype=np.float32)
        #plt.plot(data[0:4000])
        #plt.plot(data)
        #plt.show()
        return data, fs

    
    def get_IIR(self, elevation, azimuth): 
        i=str(elevation)
        print i, self.S[i]['R'], self.S[i]['L']
        dataL = np.load( self.S[i]['L']  )
        dataR = np.load( self.S[i]['R']  )
        zL = dataL['p']
        zR = dataR['p']
       
        print zL.shape, zR.shape
        # finite points from MIT experiment.
        if (np.abs(elevation)==30): 
            x=[0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 
               96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168, 
               174, 180, 186, 192, 198, 204, 210, 216, 222, 228, 234, 240, 246, 
               252, 258, 264, 270, 276, 282, 288, 294, 300, 306, 312, 318, 324, 
               330, 336, 342, 348, 354]
            if elevation in x:
                theta=x.index(elevation)
        elif (np.abs(elevation)==40): 
            x=[0, 6, 13, 19, 26, 32, 39, 45, 51, 58, 64, 71, 77, 84, 90, 96, 103,
               109, 116, 122, 129, 135, 141, 148, 154, 161, 167, 174, 180, 186, 
               193, 199, 206, 212, 219, 225, 231, 238, 244, 251, 257, 264, 270, 276,
               283, 289, 296, 302, 309, 315, 321, 328, 334, 341, 347, 354]
            if elevation in x:
                theta=x.index(elevation)
        else: 
            x=range(0,355,5)
            if elevation in x:
                theta=x.index(elevation)

        dL = zL[:,theta]
        dR = zR[:,theta]


        print "dL=",dL
        print "dR=",dR
        
        
        return dL, dR



    def localize_sound(self, elevation, azimuth): 
        dL, dR = self.get_IIR( elevation, azimuth)

        """  alg for convolution with IIR
             * use scipy to convolve input signal with impulse response
             * normalize levels to input signal
        """
        #left = scipy.signal.lfilter(dL.astype(float), 10*np.ones(dL.size), self.inputSound) / self.inputSound.shape[0]
        left = scipy.signal.lfilter(dL, [1.0], self.inputSound) 

        #left = scipy.signal.fftconvolve(dL.astype(float), self.inputSound)/ self.inputSound.shape[0]
        left =  np.max(np.abs(self.inputSound)) * left / np.max(np.abs(left))
        #plt.plot(dL.astype(float),'b-')
        #plt.show()

        right = scipy.signal.lfilter(dR.astype(float), [1.0], self.inputSound)
        right = np.max(np.abs(self.inputSound)) *right / np.max(np.abs(right))

        #plt.plot(left,'b-', right, 'g-', self.inputSound,'y-')
        #plt.plot(left,'b-')
        #plt.show()

        # Create a stereo output from left/right.
        
        signal_out = np.vstack([left, right]).transpose()
        print signal_out.shape

        filename="foo.wav"
        frmat = Format('wav')
        f = Sndfile(filename, 'w', frmat, 2, self.sampleRate)
        f.write_frames(signal_out)
        f.close()


# ------------------------------------------
if __name__ == '__main__':

    #ExprmntFiles = 'MIT_exprmnt.json'
    ExprmntFiles = 'MIT_exprmnt_npz.json'

    json_data=open( ExprmntFiles  )
    S = json.load( json_data )
    json_data.close()

    #T = HRIRTransform( S, "Flute.wav" )
    T = HRIRTransform( S, "Trombone.wav")
    T.localize_sound( 0, 125)
