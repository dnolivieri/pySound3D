#!/usr/bin/env python

##  modified 18-march
##    dnolivieri.net

##   pysigbench07.py
#      Real-time signals...(like scope)


import os
import platform
import sys

from PyQt4 import Qt,QtCore,QtGui
from PyQt4.QtCore import SIGNAL
from SignalPlot import signalPlot
from SignalWidget import signalWidget
from SignalAnalysis import sigAnalysis02
import numpy

__version__ = "1.0.0"

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.filename = None

        self.listWidget   = QtGui.QListWidget()
        self.signalArea   = signalWidget()
        self.browser      = QtGui.QTextBrowser()

        self.mainSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        self.mainSplitter.addWidget(self.signalArea)
        self.mainSplitter.addWidget(self.browser)

        self.setCentralWidget(self.mainSplitter)

        self.mainSplitter.setStretchFactor(0,3)
        self.mainSplitter.setStretchFactor(1,1)


        logDockWidget = QtGui.QDockWidget("Analysis History", self)
        logDockWidget.setObjectName("LogDockWidget")
        logDockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|
                                      QtCore.Qt.RightDockWidgetArea)



        logDockWidget.setWidget(self.listWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, logDockWidget)

        self.sizeLabel = QtGui.QLabel()
        self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLabel)
        status.showMessage("Ready", 5000)



        ## -- Actions ----
        fileNewAction = self.createAction("&New...", self.fileNew,QtGui.QKeySequence.New, 
                                          "filenew", "Create file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,QtGui.QKeySequence.Open, 
                                           "fileopen","Open an existing file")
        fileSaveAction = self.createAction("&Save", self.fileSave,QtGui.QKeySequence.Save, 
                                           "filesave", "Save the image")
        fileSaveAsAction = self.createAction("Save &As...",self.fileSaveAs, 
                                             icon="filesaveas",tip="Save using new name")

        fileGetDataAction = self.createAction("&GetData", self.fileGetData,None, 
                                            "filegetdata", "Get Data")
        

        filePrintAction = self.createAction("&Print", self.filePrint,QtGui.QKeySequence.Print, 
                                            "fileprint", "Print")
        fileQuitAction = self.createAction("&Quit", self.close,"Ctrl+Q", "filequit", 
                                           "Close the application")


        view1Action = self.createAction("&View1",self.view1, None, "view1" )
        view2Action = self.createAction("V&iew2", self.view2, None, "view2" )

        control1Action = self.createAction("&Control1",self.control1,None,"control1")
        control2Action = self.createAction("C&ontrol2", self.control2,None,"control2")

        analysis1Action = self.createAction("&Analysis1",self.analysis1, None, "analysis1")
        analysis2Action = self.createAction("A&nalysis2", self.analysis2, None, "analysis2" )


        helpAboutAction = self.createAction("&About pySigBench",self.helpAbout, None, "helpabout", "About pySigBench")
        helpHelpAction = self.createAction("&Help", self.helpHelp, QtGui.QKeySequence.HelpContents, "helpfile", "Help Document")



        ## -- Menu Definitions
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (fileNewAction, fileOpenAction,
                fileSaveAction, fileSaveAsAction, fileGetDataAction, None, filePrintAction,
                fileQuitAction)
        self.addActions(self.fileMenu, self.fileMenuActions)

        viewMenu = self.menuBar().addMenu("&View")
        self.addActions(viewMenu, (view1Action, view2Action))

        controlMenu = self.menuBar().addMenu("&Control")
        self.addActions(controlMenu, (control1Action, control2Action))

        analysisMenu = self.menuBar().addMenu("&Analysis")
        self.addActions(analysisMenu, (analysis1Action, analysis2Action))

        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))


        ## --- toolbar

        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      fileSaveAsAction))


        controlToolbar = self.addToolBar("Control")
        controlToolbar.setObjectName("ControlToolBar")
        self.addActions(controlToolbar, (control1Action, 
                                         control2Action))




        self.connect(self.signalArea, SIGNAL("plusClicked()"),self.plusZoomClicked)
        self.connect(self.signalArea, SIGNAL("minusClicked()"),self.minusZoomClicked)
        self.connect(self.signalArea, SIGNAL("restoreClicked()"),self.restoreZoomClicked)

        self.connect(self.signalArea, SIGNAL("addSignal"),self.slotaddSignal)
        self.connect(self.signalArea.sigplot[0], SIGNAL("namecheck"),self.slotaddSignal2)
        self.connect(self.signalArea.sigplot[1], SIGNAL("namecheck"),self.slotaddSignal2)

        self.connect(self.signalArea, SIGNAL("loadedSWidget()"),self.slotSWidget)


        self.connect(self.signalArea.sigplot[0], SIGNAL("slotscaleData(int)"),self.slotscaleData)
        self.connect(self.signalArea.sigplot[0], SIGNAL("signalPainter(int)"),self.slotPainter)


    def slotBrowser(self, sIndex):
        ##  determine when this can be plotted...
        ix = self.signalArea.sigplot[sIndex].Sindx
        jx = self.signalArea.sigplot[sIndex].Eindx
        text = QtCore.QString("Signal {0}: range selected:({1} - {2})   indx:({3}  {4})".format(sIndex, 
                                                              self.signalArea.sigplot[sIndex].xs1,
                                                              self.signalArea.sigplot[sIndex].xs2,
                                                              self.signalArea.sigplot[sIndex].zdata[0,ix],
                                                              self.signalArea.sigplot[sIndex].zdata[0,jx]))
        #text = QtCore.QString("something")
        self.browser.append(text)



        
    
    def slotaddSignal(self,val):
        text = QtCore.QString(val)
        self.browser.append(text)

    def slotaddSignal2(self, val1, val2):
        text = QtCore.QString("{0} {1}".format(val1, val2))
        self.browser.append(text)


    def slotSWidget(self):
        text = QtCore.QString("SWiget Constructor")
        self.listWidget.addItem(text)        




    def slotscaleData(self, val1):
        text = QtCore.QString("{0} ".format(val1))
        self.browser.append(text)

    def slotPainter(self, val1):
        text = QtCore.QString("Painter Count: {0} ".format(val1))
        self.browser.append(text)



    def plusZoomClicked(self): 
            self.browser.append("plusClicked")

    def minusZoomClicked(self): 
            self.browser.append("minusClicked")

    def restoreZoomClicked(self): 
            self.browser.append("restoreClicked")


    def setSigConnections(self):
        ## this needs to be setup after the signals are in place!!!  How do I do this!
        for i in range(self.signalArea.NumSignals):
            self.connect(self.signalArea.sigplot[i], SIGNAL("selsigdata"),self.slotBrowser)



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


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)




    def closeEvent(self, event):
        pass
    def okToContinue(self):
        pass
    def loadInitialFile(self):
        pass
    def updateStatus(self, message):
        pass
    def updateFileMenu(self):
        pass
    def fileNew(self):
        pass

    def fileOpen(self):
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        formats = (['*.wav','*.mp3'])
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
                "signals - Choose signal", dir,
                "signal files ({0})".format(" ".join(formats))))
        if fname:
            self.loadFile(fname)


    def loadFile(self, fname=None):
         if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = unicode(action.data().toString())
                if not self.okToContinue():
                    return
            else:
                return
         if fname:
            self.filename = None
            self.listWidget.addItem("LoadFile call")
            self.listWidget.addItem(fname)
            self.signalArea.addSignal(fname) 
            self.setSigConnections()


    def addRecentFile(self, fname):
        pass
    def fileSave(self):
        pass
    def fileSaveAs(self):
        pass
    def filePrint(self):
        pass


    def fileGetData(self):
        pass


    def view1(self):
        pass
    def view2(self):
        pass

    def control1(self):
        pass
    def control2(self):
        pass

    def analysis1(self):
        plotx = sigAnalysis01()
        plotx.show()
        pass

    def analysis2(self):
        # must define some way of knowing which signal is selected. 
        # this can be done later... For now, just figure out how 
        # to pass values...(write to a file)
        sIndex = 0
        ix = self.signalArea.sigplot[sIndex].Sindx
        jx = self.signalArea.sigplot[sIndex].Eindx
        npts = numpy.abs(ix - jx)
        vdata = numpy.zeros((2,npts+1))  
        for i in range(npts+1):
            k=i+ix
            vdata[0,i] = self.signalArea.sigplot[sIndex].zdata[0,k]
            vdata[1,i] = self.signalArea.sigplot[sIndex].zdata[1,k]

        fbar= open("vdata.txt", "w")
        for i in range(npts):
            line= "%d %f %f \n" %  (i, vdata[0,i], vdata[1,i])
            fbar.write(line)
        fbar.close()

        plotx = sigAnalysis02(vdata)
        plotx.show()



    def showImage(self, percent=None):
        pass



    def helpAbout(self):
        QtGui.QMessageBox.about(self, "About pySigBench",
                """<b>Python Signal Bench</b> v {0}
                <p>Copyright &copy; 2010 dnolivieri. 
                All rights reserved.
                <p>.A signal/video analysis platform
                <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
                platform.system()))


    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()



def main():
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("dnolivieri")
    app.setOrganizationDomain("uvigo.es")
    app.setApplicationName("pySound3D")
    app.setWindowIcon(QtGui.QIcon(":/icon.png"))
    form = MainWindow()
    form.resize(900,500)
    form.show()
    app.exec_()


main()
