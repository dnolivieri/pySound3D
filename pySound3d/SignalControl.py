"""
  tstsignalPlot02: 
  D.Olivieri (updated 23.march.2010)
  version 1.0.0
   - some amount of problems with speed...




"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from PyQt4 import Qt,QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from math import *
from random import random
import numpy,signal,os,wave
from numpy import vstack, hstack, eye, ones, zeros, linalg, \
newaxis, r_, flipud, convolve, matrix, array



class signalControl(QtGui.QWidget):
    def __init__(self, index, sigfilename=None, parent=None):
        super(signalControl, self).__init__(parent)
        #self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
        #                               QtGui.QSizePolicy.Expanding))

        self.widget = QtGui.QWidget(self)
        #self.widget.setGeometry(QtCore.QRect(51, 31, 111, 101))

        self.verticalLayout = QtGui.QVBoxLayout(self.widget)   
        self.radioButton = QtGui.QRadioButton(self.widget)     

        self.verticalLayout.addWidget(self.radioButton)        
        self.radioButton_2 = QtGui.QRadioButton(self.widget)   

        self.verticalLayout.addWidget(self.radioButton_2)      
        self.horizontalLayout = QtGui.QHBoxLayout()

        self.dial = QtGui.QDial(self.widget)
        self.dial.setFixedSize (40, 40)


        self.horizontalLayout.addWidget(self.dial)
        self.dial_2 = QtGui.QDial(self.widget)
        self.dial_2.setFixedSize (40, 40)

        self.horizontalLayout.addWidget(self.dial_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setLayout(self.verticalLayout)
