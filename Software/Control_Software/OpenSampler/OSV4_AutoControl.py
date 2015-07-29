#-------------------- NOTES--------------------------------------------------
# program by Frank Krijnen
# tested on Windows XP & 7
# needs Python (2.7) and pyserial

from PyQt4 import QtGui, QtCore
import sys
import numpy
import serial
import time
import datetime
import os
import ctypes

myappid = 'HoloseraINC.OpenSampler.v4.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

#----------------------------------------------------------------------------
#__________________ USER SETTINGS____________________________________________
#----------------------------------------------------------------------------

class Settings():
    # time  (minutes) that each port is sampled (8)
    samplingMinutes=0.1
    # COMMUNICATION SETTINGS (look in Control Panel and look for Arduino Mega)
    comPortOpenSampler=10
    # baudrate to OpenSampler (11500)
    baudRateOpenSampler=115200
    # amount sample positions 
    amountPositions=120
    # X positions in mm
    xmm=[26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,26,45,64,83,102,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,135,154,173,192,211,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320,244,263,282,301,320]
    # Y positions in mm
    ymm=[0.3,0.3,0.3,0.3,0.3,19.3,19.3,19.3,19.3,19.3,38.3,38.3,38.3,38.3,38.3,57.3,57.3,57.3,57.3,57.3,76.3,76.3,76.3,76.3,76.3,95.3,95.3,95.3,95.3,95.3,114.3,114.3,114.3,114.3,114.3,133.3,133.3,133.3,133.3,133.3,0.3,0.3,0.3,0.3,0.3,19.3,19.3,19.3,19.3,19.3,38.3,38.3,38.3,38.3,38.3,57.3,57.3,57.3,57.3,57.3,76.3,76.3,76.3,76.3,76.3,95.3,95.3,95.3,95.3,95.3,114.3,114.3,114.3,114.3,114.3,133.3,133.3,133.3,133.3,133.3,0.3,0.3,0.3,0.3,0.3,19.3,19.3,19.3,19.3,19.3,38.3,38.3,38.3,38.3,38.3,57.3,57.3,57.3,57.3,57.3,76.3,76.3,76.3,76.3,76.3,95.3,95.3,95.3,95.3,95.3,114.3,114.3,114.3,114.3,114.3,133.3,133.3,133.3,133.3,133.3]

    # down movement to get correct needle penetration
    needleDepth=25;
    # how far to lift up needle for moves (0 is all the way up)
    zUp=0
    # how often to send commands to keep valves in current position (55)
    solenoidRefreshTime=55
    # message to turn on flushing 
    flushingOnMessage=('M106')
    flushingOffMessage=('M107')
    # message to turn on LED BACKLIGHT 
    backlightOnMessage=('M206 S255.0')
    backlightOffMessage=('M206 S0.0')
    # message to turn off motors
    motorsOffMessage=('M84')
    # folder to save the logfile (it will be saved in a subfolder per day, same as FTIR data)
    logFilePath="C:/OpenSampler/SAMPLELOG/"
    sampleListPath="C:/OpenSampler/SAMPLELISTS/"
    
class Automation():
    error=False
    isRunning=False
    isHomed=False
    isFlushing=False

    timeLastSolenoidRefresh=time.time()
    sampleRoutineStep=0
    waitTimeSeconds=0
    waitTimeStarted=0
    startAt=-1
    sampleListRow=0
    

#---------------------------------------------------------------------------------------------
#____________________ MAIN routine______________________________________________________________
#----------------------------------------------------------------------------------------------
# each sample starts at "sampleRoutineStep=1", increase the sampleRoutineStep after every wait (otherwise only the first part
# of the code will ever be executed)

def sampleRoutine():
    # get the position and samplenumber of the sample
    try:
        position=int(controllerGui.sampleModel.data(controllerGui.sampleModel.index(Automation.sampleListRow,0)))
        print "position:" + str(position)
        samplenumber=Automation.sampleListRow+1
    except:
        print "error"
        
    if (Automation.sampleRoutineStep==1):
        print "Automation.sampleRoutineStep 1"
        GoPosition(position)
        FlushingOn()
        setGreenLabel("Running:Pre-Flush N2 #" + str(samplenumber) )
        waitseconds(3)

    elif (Automation.sampleRoutineStep==2):
        print "Automation.sampleRoutineStep 2"
        FlushingOff()
        GoZ(Settings.needleDepth)
        savetologfile()
        setGreenLabel("Running(Sampling) #" + str(samplenumber))
        waitseconds(Settings.samplingMinutes*60)   
        
    elif (Automation.sampleRoutineStep==3):
        print "Automation.sampleRoutineStep 3"
        GoZ(0.0)
        setGreenLabel("Running(Post-Flush) #" + str(samplenumber))
        waitseconds(3)

    elif (Automation.sampleRoutineStep==4):
        print "Automation.sampleRoutineStep 4"
        setGreenLabel("Running(Done) #" + str(samplenumber))     
        nextsample()

    elif (Automation.sampleRoutineStep==99):
        print "Automation.sampleRoutineStep 99"
        FlushingOff()      
        setBlueLabel("done")
        stopautom()
        waitseconds(Settings.samplingMinutes*60)   
    else:
        Automation.error=True
        print "ERROR! DID NOTHING Automation.sampleRoutineStep = " +str (Automation.sampleRoutineStep)

def setGreenLabel(text):
    controllerGui.automationMessage.setText("<span style='font-size:14pt; font-weight:600; color:#00aa00;'>" + str(text) + "</span>")
def setBlueLabel(text):
    controllerGui.automationMessage.setText("<span style='font-size:14pt; font-weight:600; color:#0000aa;'>" + str(text) + "</span>")
def setRedLabel(text):
    controllerGui.automationMessage.setText("<span style='font-size:14pt; font-weight:600; color:#FF0000;'>" + str(text) + "</span>")    
    
#---------------------------------------------------------------------------------------------
#____________________ Sub routines______________________________________________________________
#----------------------------------------------------------------------------------------------
def startAutomation(): 
    Automation.isRunning=True
    Automation.waitTimeSeconds=0
    Automation.sampleRoutineStep=0
   
    if Automation.startAt<1:
        Automation.sampleListRow=0
    else:
        Automation.sampleListRow=Automation.startAt
    for i in range(Automation.sampleListRow, controllerGui.sampleModel.rowCount()):
        controllerGui.sampleModel.setData(controllerGui.sampleModel.index(i,3),"not done")  
        
    now = datetime.datetime.now()
    print "Automation started at:" + str(now.strftime("%Y-%m-%d %H:%M"))
    serial2OpenSampler(Settings.backlightOnMessage)
    GoHome()     
    keepAnEyeOnTime()
   
def stopAutomationNow():
   Automation.isRunning=False
   serial2OpenSampler("G28")
   serial2OpenSampler(Settings.backlightOffMessage)
   FlushingOff()
   serial2OpenSampler(Settings.motorsOffMessage)
   now = datetime.datetime.now()
   print "Automation stopped at:" + str(now.strftime("%Y-%m-%d %H:%M"))
  

def keepAnEyeOnTime(): 
    # if sampling
    if Automation.isRunning :
        if (time.time()-Automation.waitTimeStarted > Automation.waitTimeSeconds):
            if (Automation.sampleRoutineStep<99):
                Automation.sampleRoutineStep=Automation.sampleRoutineStep+1
            sampleRoutine()
        else:
            secondswaited=time.time()-Automation.waitTimeStarted
            controllerGui.statusBar().showMessage("waited "+ str(int(secondswaited)) + " out of " + str(Automation.waitTimeSeconds) + "sec")
    # if the stop button is pressed
    else:
        return
          
    # solenoid valves switch off automatically after 1 minute, so send them an update sooner than that (55seconds)
    if (time.time()-Automation.timeLastSolenoidRefresh > Settings.solenoidRefreshTime):
        print "time for solenoid refresh"
        refreshsolenoids()
    # do this every 250ms as long as automation is running
    QtCore.QTimer.singleShot(250, keepAnEyeOnTime)  

def waitseconds(waitseconds):
   Automation.waitTimeStarted=time.time()
   Automation.waitTimeSeconds=waitseconds
   # try:
      # print "recieved :" + OpenSamplerSer.readline()
   # except:
      # ()
   
def nextsample():
    print "Automation.sampleListRow :" + str(Automation.sampleListRow)
    print "done sample on row :" + str(Automation.sampleListRow+1)    
    controllerGui.sampleModel.setData(controllerGui.sampleModel.index(Automation.sampleListRow,3),"DONE") 
    stopNow=str(controllerGui.sampleModel.data(controllerGui.sampleModel.index(Automation.sampleListRow,2)) )

    if stopNow == "x":
        print "stopping after line: " + str(Automation.sampleListRow +1)
        setBlueLabel("stopped after line: " + str(Automation.sampleListRow +1 ))
        Automation.isRunning=False
        Automation.sampleListRow=0
        Automation.sampleRoutineStep=99       
        stopAutomationNow()      
    elif Automation.sampleListRow +2 > controllerGui.sampleModel.rowCount():
        print "no more lines: stopping"
        Automation.isRunning=0
        Automation.sampleListRow=0
        Automation.sampleRoutineStep=99
        setBlueLabel("stopped sample list finished")
        stopAutomationNow()
    else :
        Automation.sampleRoutineStep=0
        Automation.sampleListRow=Automation.sampleListRow+1
    
def serial2OpenSampler(data2send):
    try:
        OpenSamplerSer.write(data2send+'\r')   
        print "sent to OpenSampler: " + data2send  
    except:
        setRedLabel("ERROR: COULD NOT SEND SERIAL DATA") 
        Automation.error=True
        print "error sending to OpenSampler"
    try:
        print "recieved: " + OpenSamplerSer.readline()
    except:
        ()

def GoHome():
    serial2OpenSampler("G28")
    print "going home waiting 10seconds"
    waitseconds(10)
    Automation.isHomed=True
   
def GoPosition(gotopos):
    if (gotopos > 0 and gotopos < Settings.amountPositions+1 ):
        GoZ(Settings.zUp)
        GoXYZ(Settings.xmm[gotopos-1],Settings.ymm[gotopos-1],Settings.zUp)
      
def GoXYZ(x,y,z):
    if not Automation.isHomed:
        GoHome()
    serial2OpenSampler("G1 X" + str(float(x)+0.01) + " Y" + str(float(y)+0.01) + " Z" + str(float(z)+0.01) + " F3000.0")

def GoZ(z):
    if not Automation.isHomed:
        GoHome()
    serial2OpenSampler("G1 Z" + str(float(z)+0.01) + " F3000.0")
      
def FlushingOn():
    Automation.isFlushing=True
    serial2OpenSampler(Settings.flushingOnMessage)

def FlushingOff():
    Automation.isFlushing=False
    serial2OpenSampler(Settings.flushingOffMessage)
         
def refreshsolenoids():
    Automation.timeLastSolenoidRefresh=time.time()
    if Automation.isFlushing:
        serial2OpenSampler(Settings.flushingOnMessage)     
    else:
        serial2OpenSampler(Settings.flushingOffMessage)


def savetologfile():
    curtimestruct=time.localtime()
    curyearmonthday=time.strftime("%Y%m%d", curtimestruct)
    curyear=time.strftime("%Y", curtimestruct)
    curmonth=time.strftime("%m", curtimestruct)
    curday=time.strftime("%d", curtimestruct)
    curhour=time.strftime("%H", curtimestruct)
    curminute=time.strftime("%M", curtimestruct)
    cursecond=time.strftime("%S", curtimestruct)
    curtime=time.strftime("%H:%M:%S", curtimestruct)
    logfilename=str(Settings.logFilePath) + str(curyearmonthday) + "/switcherlog.csv" 
    logfilenamedir=str(Settings.logFilePath) + str(curyearmonthday)
   
    position=int(controllerGui.sampleModel.data(controllerGui.sampleModel.index(Automation.sampleListRow,0)))
    samplename=str(controllerGui.sampleModel.data(controllerGui.sampleModel.index(Automation.sampleListRow,1)))
    position=str(position).zfill(2)
   
    if os.path.exists(logfilename): 
        openlogfile = file(logfilename, "a") 
    else:
        if not os.path.exists(logfilenamedir): 
            os.makedirs(logfilenamedir)
        openlogfile = file(logfilename, "w")
        openlogfile.write("Year,Month,Day,Hour,Minute,Second,Port,SampleName\n")
    openlogfile.write(curyear + "," + curmonth + "," + curday + "," + curhour + "," + curminute + "," + cursecond + "," + position + "," + samplename + "\n")
    openlogfile.close()
    
#--------------------------------------------------------------------------------------------------------------
#___________________________ Qt datamodel for interaction between gui and program______________________________
#--------------------------------------------------------------------------------------------------------------     

class SampleTableModel(QtCore.QAbstractTableModel):
    def __init__(self, samples = [[]], headers = [], parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.__samples = samples
        self.__headers = headers
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.__samples)
    
    def columnCount(self,parent):
        return 4
        
    def data(self, index, role = QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole:
            value = self.__samples[row][column]
            return value
        elif role == QtCore.Qt.EditRole:
            value = self.__samples[row][column]
            return value
                 
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.__headers[section]
            else:
                return section+1
                
    def flags(self, index):
        column = index.column()
        if column < 3:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if column ==0:
                (tempvalue,isint)=value.toInt()
                print tempvalue
                if tempvalue > Settings.amountPositions or tempvalue < 1:
                    return False
                else:
                    self.__samples[row][column] = tempvalue
                    self.dataChanged.emit (index, index)
                    return True
            elif column == 1:
                self.__samples[row][column] = value
                self.dataChanged.emit (index, index)
                return True
            elif column == 2:
                tempvalue=value.toString().simplified()
                if tempvalue.length()>0:
                    tempvalue="x"
                self.__samples[row][column] = tempvalue
                self.dataChanged.emit (index, index)
                return True
            elif column == 3:
                self.__samples[row][column] = value
                self.dataChanged.emit (index, index)
                return True
            return False          
    
    def setDataRow(self,row,values):
        if row > len(self.__samples) -1 :
            self.insertRows(row,1)
        self.__samples[row][0] = QtCore.QString(str(values[0]))
        self.__samples[row][1] = QtCore.QString(values[1])
        self.dataChanged.emit (self.index(row,0), self.index(row,1))
            
    def setRowCount(self, rows, parent = QtCore.QModelIndex()):
        curRowCount=len(self.__samples)
        if curRowCount > rows:
            self.removeRows(rows,curRowCount-rows)
        if curRowCount < rows:
            self.insertRows(curRowCount,rows-curRowCount)

    def insertRows(self, position, rows, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        emptyline=["1","sample","","not done"]
        for i in range(rows):
            self.__samples.insert(position, emptyline )
        self.endInsertRows()
        
    def removeRows(self,position, rows, parent = QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            value = self.__samples[position]
            self.__samples.remove(value)       
        self.endRemoveRows()
 
#--------------------------------------------------------------------------------------------------------------
#___________________________ MAIN GUI WINDOW __________________________________________________________________
#-------------------------------------------------------------------------------------------------------------- 
 
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('OpenSampler Controller')
        self.resize(500, 900)
    
        newAction = QtGui.QAction(QtGui.QIcon('icons/new.png'), 'New', self) 
        newAction.setStatusTip('New samplelist')
        newAction.triggered.connect(self.newSampleList)
        
        openAction = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
        openAction.setStatusTip('Open samplelist')
        openAction.triggered.connect(self.openFile)     
        
        saveAction = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
        saveAction.setStatusTip('Save samplelist')
        saveAction.triggered.connect(self.saveFile) 
       
        exitAction = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)
        
        addSampleAction = QtGui.QAction(QtGui.QIcon('icons/add.png'), 'Add samples', self)
        addSampleAction.setShortcut('Ctrl++')
        addSampleAction.setStatusTip('Add samples to samplelist')
        addSampleAction.triggered.connect(self.addSamples)
        
        deleteSampleAction = QtGui.QAction(QtGui.QIcon('icons/delete.png'), 'Delete selected samples', self)
        deleteSampleAction.setStatusTip('Delete selected sample rows')
        deleteSampleAction.triggered.connect(self.deleteSamples)  
        
        insertSampleAction = QtGui.QAction(QtGui.QIcon('icons/insert.png'), 'Insert samples', self)
        insertSampleAction.setShortcut('Ctrl+I')
        insertSampleAction.setStatusTip('Insert samples at selected rows')
        insertSampleAction.triggered.connect(self.insertSamples)        
        
        startAction = QtGui.QAction(QtGui.QIcon('icons/start.png'), 'Start', self)
        startAction.setStatusTip('Start samplelist')
        startAction.triggered.connect(self.startAutomation)

        startAtSelectedAction = QtGui.QAction(QtGui.QIcon('icons/start.png'), 'Start at selected line', self)
        startAtSelectedAction.setStatusTip('Start at selected line')
        startAtSelectedAction.triggered.connect(self.startAutomationAtSelected)
        
        stopAfterAction = QtGui.QAction(QtGui.QIcon('icons/stop.png'), 'Stop after', self)
        stopAfterAction.setStatusTip('Stop after this sample')
        stopAfterAction.triggered.connect(self.stopAutomationAfter)
        
        stopNowAction = QtGui.QAction(QtGui.QIcon('icons/stop2.png'), 'Stop Now', self)
        stopNowAction.setStatusTip('Stop immediately')
        stopNowAction.triggered.connect(self.stopAutomationNow)
        
        aboutAction = QtGui.QAction(QtGui.QIcon('icons/about.png'), 'About', self)
        aboutAction.setStatusTip('About this program')
        aboutAction.triggered.connect(self.showAboutBox)
        
        self.statusBarBottom=self.statusBar()
        self.automationMessage=QtGui.QLabel(self) 
        self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#aa0000;'>Idle (not started)</span>")
        self.statusBarBottom.addPermanentWidget(self.automationMessage)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(addSampleAction)
        editMenu.addAction(deleteSampleAction)
        editMenu.addAction(insertSampleAction)
        
        automationMenu = menubar.addMenu('&Automation')
        automationMenu.addAction(startAction)
        automationMenu.addAction(startAtSelectedAction)
        automationMenu.addAction(stopAfterAction)
        automationMenu.addSeparator()
        automationMenu.addAction(stopNowAction)
        
        aboutMenu = menubar.addMenu('&About')
        aboutMenu.addAction(aboutAction)
        
        headers=["Position","Name","StopAfter","Done"]
        #sampleData0=    [ ["1","sample1","","not done"], ["2","sample2","","not done"] ]                      
        sampleData0=[]
        
        self.sampleModel=SampleTableModel(sampleData0,headers)
        
        self.sampleView=QtGui.QTableView()
        self.sampleView.setModel(self.sampleModel)
        self.sampleView.setWindowTitle('OpenSampler Controller')
        # set app icon    
        app_icon = QtGui.QIcon()
        # app_icon.addFile('icons/oshw/16x16.png', QtCore.QSize(16,16))
        # app_icon.addFile('icons/oshw/24x24.png', QtCore.QSize(24,24))
        # app_icon.addFile('icons/oshw/32x32.png', QtCore.QSize(32,32))
        # app_icon.addFile('icons/oshw/48x48.png', QtCore.QSize(48,48))
        app_icon.addFile('icons/oshw/256x256.png', QtCore.QSize(256,256))
        self.sampleView.setWindowIcon(app_icon)
        app.setWindowIcon(app_icon)
        #self.sampleView.resize(500, 800)
        font = QtGui.QFont("Arial", 8)
        self.sampleView.setFont(font)
        self.sampleView.setColumnWidth(0, 60)
        self.sampleView.setColumnWidth(1, 250)
        self.sampleView.setColumnWidth(2, 60)
        self.sampleView.setColumnWidth(3, 60)
        self.sampleView.verticalHeader().setDefaultSectionSize(20)
        self.sampleView.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.clip = QtGui.QApplication.clipboard()
        self.setCentralWidget(self.sampleView)
        self.move(30,30)        
        
        
    def closeEvent(self, event):
        if Automation.isRunning:  
            quit_msg = "Are you sure you want to exit the program?"
            reply = QtGui.QMessageBox.question(self, 'WARNING STOPPING AUTOMATION!', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            event.accept() if reply == QtGui.QMessageBox.Yes else event.ignore()   
        else:
            event.accept()

            
    def deleteSamples(self):
        selectedRows=[]
        for idx in self.sampleView.selectedIndexes():
            selectedRows.append(idx.row()) 
        #trick to remove double selection
        selectedRows = sorted(list(set(selectedRows)))
        print "rows clean:" + str(selectedRows)    
        # backwards otherwise wrong lines get removed
        for  i in range (len(selectedRows),0,-1):
            self.sampleModel.removeRows(selectedRows[i-1],1)
      
    def insertSamples(self):
        selectedRows=[]
        for idx in self.sampleView.selectedIndexes():
            selectedRows.append(idx.row()) 
        #trick to remove double selection and sort small to large
        selectedRows = sorted(list(set(selectedRows)))
        # backwards otherwise wrong lines get removed
        for  i in range (len(selectedRows),0,-1):
            self.sampleModel.insertRows(selectedRows[i-1],1)
   
    def newSampleList(self):
        amountLines, ok = QtGui.QInputDialog.getText(self, 'New samplelist', 'Amount samples to add:') 
        stringLinesToAdd=str(amountLines)     
        if ok and stringLinesToAdd.isdigit() and int(stringLinesToAdd)>0:
            print "making new SampleList"
            self.sampleModel.setRowCount(0)
            for i in range(int(stringLinesToAdd)):
                currentPos=i+1
                while currentPos>Settings.amountPositions:
                    currentPos=currentPos-Settings.amountPositions
                self.sampleModel.setDataRow(i,[currentPos, "sample" + str(i+1)])    
 

    def addSamples(self):
        linesToAdd, ok = QtGui.QInputDialog.getText(self, 'Add lines', 'Amount lines to add:')
        stringLinesToAdd=str(linesToAdd)
        oldamountsamples=self.sampleModel.rowCount()
        if ok and stringLinesToAdd.isdigit():
            self.sampleModel.setRowCount(oldamountsamples+int(stringLinesToAdd))               
    
    def openFile(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', 'SAMPLELISTS/')
        if len(fname)>4:
            print "opening " + fname
            openFile=open(fname, 'rb')
            sampleList = numpy.genfromtxt(openFile, delimiter=',', dtype=None, names=True)
            amountSamples=len(sampleList['SampleName'])
            print "amount samples in this list" + str(amountSamples)
            self.sampleModel.setRowCount(0)
            for i in range(amountSamples):
                currentPos=i+1
                while currentPos>Settings.amountPositions:
                    currentPos=currentPos-Settings.amountPositions
                self.sampleModel.setDataRow(i,[currentPos, sampleList['SampleName'][i]])                     
            openFile.close()
        else:
            print "WARNING: No file selected"
        
            
    def saveFile(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', 'SAMPLELISTS/','*.csv')
        if len(fname)>4:
            print "saving to " + fname
            openFile=open(fname, 'wb')
            openFile.write("SampleName\n")
            for i in range(0, self.sampleModel.rowCount()):
                name=str(self.sampleModel.data(self.sampleModel.index(i,1)))
                openFile.write(name + "\n")              
            openFile.close()
        else:
            print "WARNING: No file selected"
            
    def startAutomation(self):
        if int(self.sampleModel.rowCount()) > 0 and Automation.isRunning == False:
            Automation.startAt=0
            Automation.sampleListRow=0
            self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#00aa00;'>Running (started)</span>")
            startAutomation() 
    def stopAutomationNow(self):
        if Automation.isRunning == True:
            self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#aa0000;'>Stopped (emergency)</span>")
            stopAutomationNow()
    def stopAutomationAfter(self):
        if Automation.isRunning == True:
            self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#FF6600;'>Will stop after this sample)</span>")
            controllerGui.sampleModel.setData(controllerGui.sampleModel.index(Automation.sampleListRow,2),QtCore.QVariant("x"))  
    def startAutomationAtSelected(self):
        if int(self.sampleModel.rowCount()) > 0 and Automation.isRunning == False:
            selectedRows=[]
            for idx in self.sampleView.selectedIndexes():
                selectedRows.append(idx.row()) 
            #trick to remove double selection and sort small to large
            selectedRows = sorted(list(set(selectedRows)))
            if len(selectedRows)!=1:
                self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#aa0000;'>Select a line!</span>")
            else:
                Automation.startAt=selectedRows[0]
                self.automationMessage.setText("<span style='font-size:16pt; font-weight:600; color:#00aa00;'>Running (started)</span>")
                startAutomation()
               
    def keyPressEvent(self, e):
        if (e.modifiers() & QtCore.Qt.ControlModifier):
            selectedRows=[]; selectedCols=[]
            selected=self.sampleView.selectedIndexes()       
            for idx in self.sampleView.selectedIndexes():
                selectedRows.append(idx.row()) 
                selectedCols.append(idx.column())
            #trick to remove double selection
            selectedRows = sorted(list(set(selectedRows)))
            selectedCols = sorted(list(set(selectedCols)))
            firstRow = selectedRows[0]
            firstCol = selectedCols[0]
            lastRow = selectedRows[len(selectedRows)-1]
            lastCol = selectedCols[len(selectedCols)-1]
                
            if e.key() == QtCore.Qt.Key_V:#paste
                dataOnClip=str(self.clip.text())
                dataOnClip=dataOnClip.strip('\n')
                #copied text is split by '\n' and '\t' to paste to the cells
                for r, row in enumerate(dataOnClip.split('\n')):
                    for c, text in enumerate(row.split('\t')):
                        if firstCol+c < 3:
                            self.sampleModel.setData(self.sampleModel.index(firstRow+r,firstCol+c),QtCore.QString(text))

            elif e.key() == QtCore.Qt.Key_C: #copy
                s = ""
                for r in xrange(firstRow,lastRow+1):
                    for c in xrange(firstCol,lastCol+1):
                        try:
                            s +=  str(self.sampleModel.data(self.sampleModel.index(r,c))) + "\t"
                        except AttributeError:
                            s += "\t"
                    s = s[:-1] + "\n" #eliminate last '\t'
                s = s[:-1]  #eliminate extra blank row
                self.clip.setText(s)
                
    def showAboutBox(self):
        QtGui.QMessageBox.about(self, "About OpenSampler Controller","This is control software for OpenSampler")       
 
#--------------------------------------------------------------------------------------------------------------
#___________________________ MAIN GUI LOOP ____________________________________________________________________
#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    global controllerGui
    global OpenSamplerSer
    OpenSamplerSer = serial.Serial(Settings.comPortOpenSampler-1, Settings.baudRateOpenSampler, timeout=0.5)  
    #sleep 2 seconds after opening port to controller so it can reboot
    # the serial has to be kept open otherwise it resets
    time.sleep(2)    
    app = QtGui.QApplication(sys.argv)
    #app.setStyle("cleanlooks")
    #app.setStyle("plastique")
    controllerGui= MainWindow()
    controllerGui.show()  
    sys.exit(app.exec_())

