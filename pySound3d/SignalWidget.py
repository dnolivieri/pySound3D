"""
  tstsignalwidget04.py: (updated 29 march 2010)
  signalWidget Class: 
    - A container for the signalPlot Class.
    - contains a control widget for the signal...

"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import sys
from math import *
from PyQt4 import  Qt, QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from SignalPlot import signalPlot
from SignalControl import signalControl
import qrc_resources
import numpy

LEFT, ABOVE = range(2)

SIG_HEIGHT=200


class  signalWidget(QtGui.QWidget): 
    def __init__(self, parent=None):
        super(signalWidget, self).__init__(parent)

        self.NumSignals=0
        self.zoomf=1

        plusZoomAction  = self.createAction("pluszoom",self.pluszoom,None,"pluszoom")
        minusZoomAction = self.createAction("minuszoom",self.minuszoom,None,"minuszoom")
        restoreZoomAction = self.createAction("restorezoom",self.restorezoom,None,"restorezoom")


        self.sigtoolbar = QtGui.QToolBar("Zoom")
        self.sigtoolbar.addAction(plusZoomAction)
        self.sigtoolbar.addAction(minusZoomAction)
        self.sigtoolbar.addAction(restoreZoomAction)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)


        self.scrollAreaWidget = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 800, 1219))

        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setDirection(QtGui.QBoxLayout.TopToBottom)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0,0,0,0)

        ### this is just a place-holder... 
        self.sigplot = []
        self.sigcontrol = []
        for i in range(4):
            self.sigplot.append(signalPlot(i))
            self.sigcontrol.append(signalControl(i))

                    
        self.scrollArea.setWidget(self.scrollAreaWidget)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.sigtoolbar)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)


    #------------------------------
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def pluszoom(self):
        self.emit(SIGNAL("plusClicked()"))  ##for seeing action
        ## must perform this for all signals...
        if (self.NumSignals > 0): 
            self.zoomf *=2
            for i in range(self.NumSignals):
                self.sigplot[i].resizeSignal(self.sigplot[i].width()*self.zoomf, self.sigplot[i].height())


    def minuszoom(self):
        self.emit(SIGNAL("minusClicked()"))
        if (self.NumSignals> 0):
            self.sigplot[0].resizeSignal(200,200)

    def restorezoom(self):
        self.emit(SIGNAL("restoreClicked()"))


    def addSignal(self, fname):
        self.emit(SIGNAL("addSignal"), fname)
        i = self.NumSignals

        self.sigcontrol.append(signalControl(i))
        self.sigcontrol[i].setGeometry(QtCore.QRect(51, 31, 111, 101))

        self.sigplot.append(signalPlot(i))
        self.sigplot[i].loadFile(fname)

        self.hLayout = QtGui.QHBoxLayout()
        self.hLayout.addWidget(self.sigcontrol[i])
        self.hLayout.addWidget(self.sigplot[i])

        self.verticalLayout.addLayout(self.hLayout)



        #self.verticalLayout.addWidget(self.sigcontrol[i])
        #self.sigcontrol[i].resize(200,100)
        #self.verticalLayout.addWidget(self.sigplot[i])


        self.scrollAreaWidget.resize(self.scrollAreaWidget.width(), (self.NumSignals +1) * SIG_HEIGHT)
        self.sigplot[i].resize(self.scrollAreaWidget.width(), SIG_HEIGHT)
        #self.sigplot[i].resize(self.scrollAreaWidget.width(), self.scrollAreaWidget.height())
        self.NumSignals +=1

    ## here is if we want to add more than one...
    def addSignals(self, sigfname, nsignals):
        self.NumSignals = nsignals
        self.sigplot = []
        for i in range(nsignals):
            self.sigplot.append(signalPlot(i))

        for i in range(nsignals):
            ## this doesn't work.
            self.sigActive[i] = QRadioButton()
            self.sigActive[i].setText("signal")
            hlayout = QtGui.QHBoxLayout()
            hlayout.addWidget(self.sigActive[i])
            hlayout.addWidget(self.sigplot[i])
            self.verticalLayout.addWidget(hlayout)
            self.scrollAreaWidget.resize(self.scrollAreaWidget.width(), (i+1) * SIG_HEIGHT)
            self.sigplot[i].resize(self.scrollAreaWidget.width(), SIG_HEIGHT)
            #self.sigplot[i].resize(self.scrollAreaWidget.width(), self.scrollAreaWidget.height())

        
