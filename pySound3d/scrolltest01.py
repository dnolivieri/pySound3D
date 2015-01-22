#!/usr/bin/env python

##  modified 24-march.... 1:00am
##   sigMain04.py
##    --- started from previous versions on 23-march...

import os
import platform
import sys

from PyQt4 import Qt,QtCore,QtGui
from PyQt4.QtCore import SIGNAL
from tstsignalplot02 import signalPlot
from tstsignalwidget02 import signalWidget
import numpy

class MainForm(QtGui.QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)
        
        plusZoomAction  = self.createAction("pluszoom",self.pluszoom,None,"pluszoom")
        minusZoomAction = self.createAction("minuszoom",self.minuszoom,None,"minuszoom")
        restoreZoomAction = self.createAction("restorezoom",self.restorezoom,None,"restorezoom")
        
        self.sigtoolbar = QtGui.QToolBar("Zoom")
        self.sigtoolbar.addAction(plusZoomAction)
        self.sigtoolbar.addAction(minusZoomAction)
        self.sigtoolbar.addAction(restoreZoomAction)


        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)


        self.scrollWidget = QtGui.QWidget(self.scrollArea)
        self.scrollWidget.setGeometry(QtCore.QRect(0, 0, 800, 1219))

        self.vlayout = QtGui.QVBoxLayout(self.scrollWidget)
        self.sigplot1 = signalPlot(0)
        self.sigplot2 = signalPlot(1)
        self.vlayout.addWidget(self.sigplot1)
        self.vlayout.addWidget(self.sigplot2)

        self.scrollArea.setWidget(self.scrollWidget)


        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.sigtoolbar)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)

        ##QTimer.singleShot(0, self.initialLoad)

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
        pass

    def minuszoom(self):
        pass

    def restorezoom(self):
        pass



app = QtGui.QApplication(sys.argv)
form = MainForm()
form.resize(850, 620)
form.show()
app.exec_()

