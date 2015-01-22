#!/usr/bin/env python
"""
    dnolivieri:
      - code for converting between mats and npz.
    
"""

import numpy as np
import scipy.io
import time
import bisect
import os, fnmatch
import glob
import sys
import re

import itertools
import json

class HRIRTransformMgr:
    def __init__(self, S):
        self.S = S
        

    def cnvrt_mats_npz(self):
        for i in self.S.iterkeys():
              print i, self.S[i]['R'], self.S[i]['L']

              matL = scipy.io.loadmat( self.S[i]['L'] )
              H = matL['H']
              H=H.astype(int)
              Hmat_out="L"+ str(i) + ".npz"
              np.savez(Hmat_out, p = H )

              matR = scipy.io.loadmat( self.S[i]['R'] )
              R = matR['R']
              R=R.astype(int)
              Rmat_out="R"+ str(i) + ".npz"
              np.savez(Rmat_out, p = R )

       

# ------------------------------------------
if __name__ == '__main__':

    #ExprmntFiles = 'MIT_exprmnt.json'
    ExprmntFiles = 'MIT_exprmnt_npz.json'

    json_data=open( ExprmntFiles  )
    S = json.load( json_data )
    json_data.close()

    T = HRIRTransformMgr( S )
    T.cnvrt_mats_npz()
