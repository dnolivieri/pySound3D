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
import wavfile as wv
from numpy import vstack, hstack, eye, ones, zeros, linalg, \
newaxis, r_, flipud, convolve, matrix, array


H1_OFFSET=10
H2_OFFSET=2
W1_OFFSET=28
W2_OFFSET=5

TIC_SIZE = 4
N_YTICS = 4
N_XTICS = 8

SIG_HEIGHT=100

class signalPlot(QtGui.QWidget):
    def __init__(self, index, sigfilename=None, parent=None):
        super(signalPlot, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Expanding))

        self.index = index
        self.isDataLoaded = False
        self.isScaled=False
        self.setMinimumSize(self.minimumSizeHint())
        self.justDoubleClicked = False
        self.selectMode=False
        self.selStartPos=0
        self.selEndPos=0
        self.xStart=0
        self.xEnd=0
        self.xs1=0
        self.xs2=0
        self.paintercount=0
        self.Sindx=0
        self.Eindx=0

    def loadFile(self, sigfilename):
        if sigfilename == None:
            self.Npts = 200
        else: 
            self.sigfilename = sigfilename
            indata = wv.read_wavfile(sigfilename)
            self.sigdata = numpy.asarray(indata[0][:])
            self.Npts = self.sigdata.size
            self.emit(SIGNAL("namecheck"), sigfilename, self.Npts)
            #self.sdata = Qt.QPolygonF()
            self.sdata = Qt.QPolygon()
            self.zdata = numpy.zeros((2,self.Npts))
            self.isDataLoaded = True
            self.setData()





    def resizeSignal(self,x,y):
        self.resize(x,y)
        self.update()

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def minimumSizeHint(self):
        return QtCore.QSize(100, 100)


    def mousePressEvent(self, event):
        self.text = QtCore.QString("{0} {1}".format(
                self.sdata[0].x(),self.sdata[0].y()))

        if self.selectMode == False:
            self.selectMode=True
            self.selStartPos = event.pos().x()
            self.selEndPos = self.selStartPos
        self.update()

    def mouseReleaseEvent(self, event):
        if self.selectMode:
            self.selectMode = False
            self.selEndPos = event.pos().x()
            self.update()

    def mouseMoveEvent(self, event):
        if self.selectMode:
            self.selEndPos = event.pos().x()
            self.update()


    def mouseDoubleClickEvent(self, event):
        if not self.justDoubleClicked:
            self.justDoubleClicked = True
        else:
            self.justDoubleClicked = False
        self.update()


    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        self.emit(SIGNAL("signalPainter(int)"), self.paintercount)
        self.paintercount+=1
        if (self.isDataLoaded == True):
            self.plot_signal(painter)
            self.plot_mkXticlabels(painter)
            self.plot_mkYticlabels(painter)
            if (self.selEndPos != self.selStartPos):
                self.shade_selsignal(painter)



    def plot_signal(self, painter):
        if (self.isScaled==False): 
            self.scaledData()
            self.isScaled=True

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        x = int(self.sdata[0].x())
        y = int(self.sdata[0].y())
        color = QtCore.Qt.red
        painter.save()
        painter.setPen(QtCore.Qt.black)
        painter.drawLine(QtCore.QPoint(W1_OFFSET,H2_OFFSET), QtCore.QPoint(W1_OFFSET,self.height()-H1_OFFSET))
        painter.drawLine(QtCore.QPoint(W1_OFFSET,self.height()-H1_OFFSET), QtCore.QPoint(self.width()-W2_OFFSET,self.height()-H1_OFFSET))


        if self.justDoubleClicked:        
            painter.setPen(QtCore.Qt.green)
        else:
            painter.setPen(QtCore.Qt.blue)

        painter.drawPolyline(self.sdata)
        painter.restore()
        painter.fillRect(QtCore.QRectF(0,self.height()-H1_OFFSET,self.width(),H1_OFFSET),QtGui.QBrush(QtGui.QColor(239,239,239)));


    def plot_mkYticlabels(self, painter):
        zmax= self.zdata[1,:].max()
        zmin= self.zdata[1,:].min()        
        Delta = zmax - zmin
        
        font = QtGui.QFont()
        font.setStretch(QtGui.QFont.Condensed)
        font.setPointSize(9)
        painter.setFont(font);

        """ -- this has to be fixed """
        ny= N_YTICS
        zbar=zmax
        DeltaZ = self.height()
        wz=H2_OFFSET
        while zbar > zmin:
            painter.save()
            #painter.drawText(QtCore.QPointF(1,wz), QtCore.QString("%1").arg(zbar));
            painter.drawLine(QtCore.QPoint(W1_OFFSET-TIC_SIZE,wz), QtCore.QPoint(W1_OFFSET,wz))
            painter.restore()
            zbar-=Delta/ny
            wz += DeltaZ/ny


    def plot_mkXticlabels(self, painter):
        font = QtGui.QFont()
        font.setStretch(QtGui.QFont.Condensed)
        font.setPointSize(9)
        painter.setFont(font);

        w1 = W1_OFFSET
        w2 = self.width()-W2_OFFSET
        x1 = self.zdata[0,:].min()
        x2 = self.zdata[0,:].max()

        dW = w2-w1
        dX = x2-x1


        ### make these global variables...
        nx= N_XTICS
        xtic = w1
        xval = x1
        while xtic < w2:
            xtic+=dW/nx
            xval+=dX/nx
            painter.save()
            painter.drawText(QtCore.QPointF(xtic-8,self.height()-10),QtCore.QString("%1").arg(xval));
            painter.drawLine(QtCore.QPoint(xtic,self.height()-H1_OFFSET-TIC_SIZE/2), QtCore.QPoint(xtic,self.height()-H1_OFFSET+TIC_SIZE/2))
            painter.restore()



    def shade_selsignal(self,painter):
        if ( (self.selEndPos != 0) or (self.selStartPos != 0) or (self.selEndPos != self.selStartPos)):
            if (self.selEndPos > self.selStartPos):
                startTimeX = self.selStartPos
                endTimeX   = self.selEndPos
            else:
                startTimeX = self.selEndPos
                endTimeX = self.selStartPos
            painter.fillRect(QtCore.QRectF(startTimeX,0,endTimeX-startTimeX,self.height()-30),QtGui.QBrush(QtGui.QColor(49,209,253,100)));
            self.emit(SIGNAL("selSignalChange(int,int)"),self.selStartPos, self.selEndPos)
            self.set_selsigdata()


    def set_selsigdata(self):
        w1 = W1_OFFSET
        w2 = self.width()-W2_OFFSET
        x1 = self.zdata[0,:].min()
        x2 = self.zdata[0,:].max()

        xStart = ((self.selStartPos *(x2 - x1)) - (w1*x2) + (w2*x1))/(w2-w1)
        xEnd = ((self.selEndPos *(x2 - x1)) - (w1*x2) + (w2*x1))/(w2-w1)


        ## do this by searching...(later this could be a binary type search.
        Sfound=False
        Efound=False

        for i in range(self.zdata[0,:].size-1):
            if (Sfound and Efound):
                break
            if self.zdata[0,i]==xStart or (self.zdata[0,i] < xStart and self.zdata[0,i+1] >= xStart):
                self.Sindx=i
                Sfound=True
            if self.zdata[0,i]==xEnd or (self.zdata[0,i] < xEnd and self.zdata[0,i+1] >= xEnd):
                self.Eindx=i
                Efound=True

                
        ## these are all the selected points...
        ##  take this out to save time.
        npts = numpy.abs(self.Eindx - self.Sindx)
        #vdata = numpy.zeros((2,npts+1))  
        #for i in range(npts+1):
        #    k=i+self.Sindx
        #    vdata[0,i] = self.zdata[0,k]
        #    vdata[1,i] = self.zdata[1,k]

        self.xStart = xStart
        self.xEnd   = xEnd
        self.xs1=self.zdata[0,self.Sindx]
        self.xs2=self.zdata[0,self.Eindx]

        #self.emit(SIGNAL("selsigdata(int,int,int,int)"),self.xStart, self.xEnd,self.xs1, self.xs2)
        self.emit(SIGNAL("selsigdata"), self.index)
        return xStart


    def setData(self):
        for i in range(self.Npts):
            newX=W1_OFFSET + i*2
            #newY=float(random())*100
            newY=self.sigdata[i] 
            self.zdata[0,i] = newX
            self.zdata[1,i] = newY

    def scaledData(self):
        h1 = self.height()-H1_OFFSET
        h2 = H2_OFFSET
        w1 = W1_OFFSET
        w2 = self.width()-W2_OFFSET

        x1 = self.zdata[0,:].min()
        x2 = self.zdata[0,:].max()
        y1 = self.zdata[1,:].min()
        y2 = self.zdata[1,:].max()

        #logic for only painting some..
        #  still don't have this solved...
        # .... more or less this logic is ok... but could be improved...
        ##     remember it is just to visualize... the data must be obtained
        ##     from the inverse mapping...
        #vis_factor= int(self.Npts/ self.width()/4)
        vis_factor= int(self.Npts/ self.width())
        if vis_factor == 0:
            vis_factor=1

        #f = Qt.QPolygonF()
        f = Qt.QPolygon()
        for i in range(self.Npts):
            if not (i % vis_factor): 
                xs = (w1*x2-w2*x1)/(x2-x1) + self.zdata[0,i]*(w2-w1)/(x2-x1)
                ys = (h1*y2-h2*y1)/(y2-y1) + self.zdata[1,i]*(h2-h1)/(y2-y1)
                #f.append(QtCore.QPointF(xs, ys))
                f.append(QtCore.QPoint(  int(round(xs)), int(round(ys))  ))
        self.isScaled=True
        self.sdata = f
        self.emit(SIGNAL("slotscaleData(int)"), self.sdata.size())



