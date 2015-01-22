import sys
from PyQt4 import Qt,QtCore,QtGui
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import pylab
import matplotlib.pyplot as plt

class sigAnalysis02(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self, wdata=None):
        self.fig = Figure()
        #self.wdata = numpy.zeros((2,self.Npts))
        if wdata!=None: 
            self.axes = self.fig.add_subplot(111)
            self.x = wdata[0,:]
            self.y = wdata[1,:]
            self.axes.specgram(self.y)
            FigureCanvas.__init__(self, self.fig)
