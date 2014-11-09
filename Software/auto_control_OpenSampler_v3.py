#-------------------- NOTES--------------------------------------------------
# program by Frank Krijnen
# tested on Windows XP & 7
# needs Python (2.7) and pyserial

#----------------------------------------------------------------------------
#__________________ USER SETTINGS____________________________________________
#----------------------------------------------------------------------------

# time  (minutes) that each port is sampled (20)
samplingminutes=0.2

# COMMUNICATION SETTINGS
# comport to which the 1st Valco selector valve is attached (1)
comport_opensampler=6

# baudrate to valco selector valve (9600)
baudrate_opensampler=115200

# amount sample positions
amount_positions=45

# X positions in mm
xmm=[10,35,60,85,110,135,160,185,210,235,10,35,60,85,110,135,160,185,210,235,10,35,60,85,110,135,160,185,210,235,10,35,60,85,110,135,160,185,210,235,10,35,60,85,110,135,160,185,210,235]

# Y positions in mm
ymm=[10,10,10,10,10,10,10,10,10,10,35,35,35,35,35,35,35,35,35,35,60,60,60,60,60,60,60,60,60,60,85,85,85,85,85,85,85,85,85,85,110,110,110,110,110,110,110,110,110,110]

NeedleDepth=68;
zUp=0

solenoidrefreshtime=60

# message to turn on flushing 
flushing_on=('M106')
flushing_off=('M107')

# message to turn on LED BACKLIGHT 
backlight_on=('M206 S255.0')
backlight_off=('M206 S0.0')

# message to turn off motors
motors_off=('M84')

# folder to save the logfile (it will be saved in a subfolder per day, same as FTIR data)
logfilepath="C:/OpenSampler/SampleLog/"

#-----------------------------------------------------------------------------------------
#____________________________ VARIABLES_______________________________________________
#--------------------------------------------------------------------------------------
ishomed=0
flushing=0

#__________________________________________________________________________
#//////////////// DO NOT CHANGE BELOW///////////////////////////////////////
#_______________________________________________________
#------------SETUP PROGRAM---------------------------------
#_______________________________________________________
from Tkinter import *
import tkFileDialog
import time
import serial
import string
import datetime
import os
import array
import csv
import numpy

# create a root TkInter frame
root = Tk()
root.title('Automated OpenSampler controller v20140929')

running=0
timelastsolenoidrefresh=time.time()
waittimestarted=time.time()
waittime=0
samplelistopen=0

comerror=0
OpenSamplerSer = serial.Serial(comport_opensampler-1, baudrate_opensampler, timeout=2)  
#sleep 2 seconds after opening port to controller so it can reboot
# the serial has to be kept open otherwise it resets
time.sleep(2)

#---------------------------------------------------------------------------------------------
#____________________ MAIN routine______________________________________________________________
#----------------------------------------------------------------------------------------------
# each port starts at "portstatus=1", increase the portstatus after every wait (otherwise only the first part
# of the code will ever be executed)

def portroutine(port):
   global portstatus
   global currentsample
   
   if (portstatus==1):
      print "portstatus 1"
      GoPosition(port)
      FlushingOn()
      setlabel("flushing picarro with N2 before position " + str(port) )
      waitseconds(5)

   elif (portstatus==2):
      print "portstatus 2"
      FlushingOff()
      GoZ(NeedleDepth)
      savetologfile(port)
      setlabel("sampling position " + str(port) + " for " + str(samplingminutes)+ "minutes")
      waitseconds(samplingminutes*60)   
            
   elif (portstatus==3):
      print "portstatus 3"
      FlushingOn()
      GoZ(0.0)
      setlabel("backflushing with N2 before position " + str(port) )
      waitseconds(3)

   elif (portstatus==4):
      print "portstatus 4"
      setlabel("done sampling position " + str(port))  
      nextsample()
      
   elif (portstatus==99):
      print "portstatus 99"
      FlushingOff()      
      setlabel("done samplelist")
      stopautom()
      waitseconds(samplingminutes*60)   
   else:
      print "ERROR! DID NOTHING portstatus = " +str (portstatus)
   

#---------------------------------------------------------------------------------------------
#____________________ Sub routines______________________________________________________________
#----------------------------------------------------------------------------------------------
def startautom():
   global running
   global portstatus
   global waittime
   global amountsamples
   global firstsample
   global lastsample
   global currentsample
   
   waittime=0
   
   for i in range(1, amountsamples+1):
      donelist[i-1].config(text="")
   
   firstsample=beginwith.get()
   if firstsample<1:
      firstsample=1
   lastsample=endafter.get()
   if lastsample<1:
      lastsample=amountsamples 
   currentsample=firstsample
   print "starting at sample # : " + str(firstsample)
   print "ending after sample #: " + str(lastsample)
   running=1   
   portstatus=0
   now = datetime.datetime.now()
   print "Automation started at:" + str(now.strftime("%Y-%m-%d %H:%M"))
   #print "going home"
   serial2OpenSampler("G28")
   statuslabel.config(text="Automation started at: "+ str(now.strftime("%Y-%m-%d %H:%M")) )
   buttonrunfile.config(bg="green")
   buttonstopfile.config(bg="white smoke")
   serial2OpenSampler(backlight_on)
   
   keepaneyeontime()
   
def stopautom():
   global running
   serial2OpenSampler("G28")
   serial2OpenSampler(backlight_off)
   FlushingOff()
   MotorsOff()
   running=0
   now = datetime.datetime.now()
   print "Automation stopped at:" + str(now.strftime("%Y-%m-%d %H:%M"))
   statuslabel.config(text="Automation stopped at: "+ str(now.strftime("%Y-%m-%d %H:%M")) )
   buttonrunfile.config(bg="white smoke")
   buttonstopfile.config(bg="red")    

   
def keepaneyeontime():
   global currentsample
   global timelastsolenoidrefresh
   global waittimestarted
   global waittime
   global portstatus

   currentport=currentsample
   while currentport>amount_positions:
      currentport=currentport-amount_positions
   # if the stop button is pressed
   if running < 1:
      return      
   # if sampling
   else:
      if (time.time()-waittimestarted > waittime):
         if (portstatus<99):
            portstatus=portstatus+1
         portroutine(currentport)
      else:
         secondswaited=time.time()-waittimestarted
         timeleftlabel.config(text="waited "+ str(int(secondswaited)) + " out of " + str(waittime) )
          
  # solenoids switch off after 5 minutes, so send them an update every now and then
   if (time.time()-timelastsolenoidrefresh > solenoidrefreshtime):
      print "time for solenoid refresh"
      refreshsolenoids()
      
   
   
   # do this every 250ms as long as automation is running
   clock.after(250, keepaneyeontime)   

def waitseconds(waitseconds):
   global waittimestarted
   global waittime
   waittimestarted=time.time()
   waittime=waitseconds
   try:
      line = OpenSamplerSer.readline()
      print "recieved :" + line
   except:
      ()
   
def nextsample():
   global currentsample
   global portstatus
   global firstsample
   global lastsample
   lastsample=endafter.get()
   if lastsample<1:
      lastsample=amountsamples 
      
   firstsample=beginwith.get()
   if firstsample<1:
      firstsample=1
      
   donelist[currentsample-1].config(text="done")
   currentsample=currentsample+1
   if (currentsample > lastsample):
        portstatus=99
   elif (currentsample < firstsample):
      currentsample=firstsample
   else:
      portstatus=0

  
def serial2OpenSampler(data2send):
   #sys.stdout.write("send selector1: " + data2send )
   try:
      OpenSamplerSer.write(data2send+'\r')   
      print "sent to OpenSampler: " + data2send  
   except:
      errorlabel.config(text="ERROR: COULD NOT SEND SERIAL DATA")  
   try:
      line = OpenSamplerSer.readline()
      print "recieved: " + line
   except:
      ()

def GoHome():
   global ishomed
   serial2OpenSampler("G28")
   print "going home waiting 15seconds"
   waitseconds(15)
   ishomed=1
   
def GoPosition(gotopos):
   if (gotopos > 0 and gotopos < amount_positions+1 ):
      GoZ(zUp)
      GoXYZ(xmm[gotopos-1],ymm[gotopos-1],zUp)
      
def GoXYZ(x,y,z):
   global ishomed
   if ishomed<1:
      GoHome()
   serial2OpenSampler("G1 X" + str(float(x)+0.01) + " Y" + str(float(y)+0.01) + " Z" + str(float(z)+0.01) + " F3000.0")

def GoZ(z):
   global ishomed
   if ishomed<1:
      GoHome()
   serial2OpenSampler("G1 Z" + str(float(z)+0.01) + " F3000.0")
   
   
def FlushingOn():
   global flushing
   flushing=1
   serial2OpenSampler(flushing_on)

def FlushingOff():
   global flushing
   flushing=0
   serial2OpenSampler(flushing_off)
      
def MotorsOff():
    serial2OpenSampler(motors_off) 
    
def setlabel(labeltext):
   nextlabel.config(text=labeltext) 
         
def refreshsolenoids():
 global timelastsolenoidrefresh
 global flushing
 
 timelastsolenoidrefresh=time.time()
 if flushing>0:
   serial2OpenSampler(flushing_on)     
 else:
   serial2OpenSampler(flushing_off)


def savetologfile(portsampling):
   global currensample
   curtimestruct=time.localtime()
   curyearmonthday=time.strftime("%Y%m%d", curtimestruct)
   curyear=time.strftime("%Y", curtimestruct)
   curmonth=time.strftime("%m", curtimestruct)
   curday=time.strftime("%d", curtimestruct)
   curhour=time.strftime("%H", curtimestruct)
   curminute=time.strftime("%M", curtimestruct)
   cursecond=time.strftime("%S", curtimestruct)
   curtime=time.strftime("%H:%M:%S", curtimestruct)
   logfilename=str(logfilepath) + str(curyearmonthday) + "/switcherlog.csv" 
   logfilenamedir=str(logfilepath) + str(curyearmonthday)
   
   if os.path.exists(logfilename): 
      openlogfile = file(logfilename, "a") 
   else:
      if not os.path.exists(logfilenamedir): 
         os.makedirs(logfilenamedir)
      openlogfile = file(logfilename, "w")
      openlogfile.write("Year,Month,Day,Hour,Minute,Second,Port,SampleName\n")
   samplename=samplenamelist[currentsample-1].get()
   openlogfile.write(curyear + "," + curmonth + "," + curday + "," + curhour + "," + curminute + "," + cursecond + "," +str(portsampling).zfill(2)+ "," + str(samplename) + "\n")
   openlogfile.close()

def warnclose():
   print "CLOSE BUTTON IS DISABLED"
   print "JUST OPEN A DIFFERENT LIST"

def drawsamplelist(amountrows,title):
   global samplelistwindow; global samplelistopen; global amount_positions;   global amountsamples
   global j; global frame; global samplenumber;
   global portposition; global samplenamelist; global beginwithlist; global beginwith; global endafterlist; global endafter; global donelist
   samplenumber=[]; portposition=[]; samplenamelist=[]; beginwithlist=[]; beginwith = IntVar(); endafterlist=[]; endafter = IntVar(); donelist=[]
   amountsamples=amountrows
   try:
      samplelistwindow.winfo_exists()
      samplelistwindow.destroy()       
   except:
      print "no samplelist opened yet"
   
   samplelistwindow= Toplevel()
   samplelistwindow.title("Samplelist: " + str(title))
   samplelistwindow.protocol('WM_DELETE_WINDOW', warnclose)
   userResponse = ''
   
   frame = VerticalScrolledFrame(samplelistwindow)
   frame.grid(row=100, column=0,columnspan=10, sticky=NS) 

   samplenumberlabel=Label(frame.interior, text="Sample#")
   samplenumberlabel.grid(row=1,column=0, columnspan=1 )

   portlabel=Label(frame.interior, text="Position")
   portlabel.grid(row=1,column=1, columnspan=1 )

   samplelabel=Label(frame.interior, text="Samplename")
   samplelabel.grid(row=1,column=2, columnspan=4, sticky=W)

   beginlabel=Label(frame.interior, text="Start with")
   beginlabel.grid(row=1,column=7, columnspan=1 )

   endlabel=Label(frame.interior, text="Stop after")
   endlabel.grid(row=1,column=8, columnspan=1 )

   donelabel=Label(frame.interior, text="Done")
   donelabel.grid(row=1,column=9, columnspan=1 )
   j=1
   for i in range(1, amountrows+1):
      samplenumber.append(Label(frame.interior, text=str(int(i))))
      samplenumber[i-1].grid(row=(2+i),column=0, columnspan=1 )
   for i in range(1, amountrows+1):
      if j>amount_positions:
         j=j-amount_positions
      portposition.append(Label(frame.interior, text=str(int(j))))
      portposition[i-1].grid(row=(2+i),column=1, columnspan=1 )
      j=j+1
   for i in range(1, amountrows+1):
      samplenamelist.append(Entry(frame.interior, width=30))
      samplenamelist[i-1].grid(row=(2+i),column=2, columnspan=4, sticky=W)  
   for i in range(1, amountrows+1):
      beginwithlist.append(Checkbutton(frame.interior,variable=beginwith,onvalue=i))
      beginwithlist[i-1].grid(row=(2+i),column=7, columnspan=1 )
   for i in range(1, amountrows+1):
      endafterlist.append(Checkbutton(frame.interior,variable=endafter,onvalue=i))
      endafterlist[i-1].grid(row=(2+i),column=8, columnspan=1)
   for i in range(1, amountrows+1):
      donelist.append(Label(frame.interior, text=""))
      donelist[i-1].grid(row=(2+i),column=9, columnspan=1)

def addlinessamplelist():
   global amountsamples; global samplenumber; global j
   global amount_positions
   global portposition; global samplenamelist; global beginwithlist; global endafterlist; global donelist   
   global frame
      
   for i in range(amountsamples+1, amountsamples+10+1):    
      samplenumber.append(Label(frame.interior, text=str(int(i))))
      samplenumber[i-1].grid(row=(2+i),column=0, columnspan=1 )
   for i in range(amountsamples+1, amountsamples+10+1):
      if j>amount_positions:
         j=j-amount_positions
      portposition.append(Label(frame.interior, text=str(int(j))))
      portposition[i-1].grid(row=(2+i),column=1, columnspan=1 )
      j=j+1
   for i in range(amountsamples+1, amountsamples+10+1):
      samplenamelist.append(Entry(frame.interior, width=30))
      samplenamelist[i-1].grid(row=(2+i),column=2, columnspan=4, sticky=W)  
   for i in range(amountsamples+1, amountsamples+10+1):
      beginwithlist.append(Checkbutton(frame.interior,variable=beginwith,onvalue=i))
      beginwithlist[i-1].grid(row=(2+i),column=7, columnspan=1 )
   for i in range(amountsamples+1, amountsamples+10+1):
      endafterlist.append(Checkbutton(frame.interior,variable=endafter,onvalue=i))
      endafterlist[i-1].grid(row=(2+i),column=8, columnspan=1)
   for i in range(amountsamples+1, amountsamples+10+1):
      donelist.append(Label(frame.interior, text=""))
      donelist[i-1].grid(row=(2+i),column=9, columnspan=1)
   amountsamples=amountsamples+10
      
def opensamplelist():
   global samplelistwindow
   global samplelistopen
   # get filename
   fileopen_opt = options = {}
   options['defaultextension'] = '.csv' 
   options['filetypes'] = [('csv files', '.csv'),('all files', '.*')]
   options['initialdir'] = 'C:\SWITCH_CONTROL\SAMPLELISTS'
   options['initialfile'] = 'samplelist.csv'
   options['parent'] = root
   options['title'] = 'Choose a samplelist to open'
   samplelistfilename = tkFileDialog.askopenfilename(**fileopen_opt)
   
   # open file 
   if samplelistfilename :
      opensamplelistfile=open(samplelistfilename, 'rb')
      samplelist = numpy.genfromtxt(opensamplelistfile, delimiter=',', dtype=None, names=True)
      print "amount samples"      
      print len(samplelist['SampleName'])

      samplelistopen=1
      drawsamplelist(len(samplelist['SampleName'])+10,samplelistfilename)
      
      for i in range(0, len(samplelist['SampleName'])):
         samplenamelist[i].delete(0, END)
         samplenamelist[i].insert(0, samplelist['SampleName'][i])
      opensamplelistfile.close()
      
      
def newsamplelist():
   global samplelistwindow
   global samplelistopen
   class MyDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        Label(top, text="Amount samples").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
    def ok(self):
        print "value is", self.e.get()
        global amountsamples
        amountsamples=int(self.e.get())
        self.top.destroy()
   d = MyDialog(root)
   root.wait_window(d.top)
    
   print "amount samples"      
   print amountsamples

   samplelistopen=1
   drawsamplelist(amountsamples,"new samplelist")


def savesamplelist():
   # get filename
   fileopen_opt = options = {}
   options['defaultextension'] = '.csv' 
   options['filetypes'] = [('csv files', '.csv'),('all files', '.*')]
   options['initialdir'] = 'C:\SWITCH_CONTROL\SAMPLELISTS'
   options['initialfile'] = 'samplelist.csv'
   options['parent'] = root
   options['title'] = 'Choose a file to save samplelist to '
   samplelistfilename = tkFileDialog.asksaveasfilename(**fileopen_opt)
   
   # open file 
   if samplelistfilename :
      opensamplelistfile=open(samplelistfilename, 'w')
      opensamplelistfile.write("SampleName\n")
      for i in range(0, amountsamples):    
         opensamplelistfile.write(samplenamelist[i].get() + "\n")
      opensamplelistfile.close()


      
# -------------------------------------------------------------------------------------------------
#___________________ START OF GUI_________________________________________
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,
                        height=600)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
        
        
buttonrunfile=Button(root, text='START', command=startautom, bg="white smoke")
buttonrunfile.grid(row=1,column=0,columnspan=1,sticky=W)
buttonstopfile=Button(root, text='STOP', command=stopautom,bg="red")
buttonstopfile.grid(row=1,column=1,columnspan=1,sticky=W)
buttonnewfile=Button(root, text='NEW', command=newsamplelist)
buttonnewfile.grid(row=1,column=3,columnspan=1,sticky=W)
buttonopenfile=Button(root, text='OPEN', command=opensamplelist)
buttonopenfile.grid(row=1,column=4,columnspan=1,sticky=W)
buttonsavefile=Button(root, text='SAVE', command=savesamplelist)
buttonsavefile.grid(row=1,column=5,columnspan=1,sticky=W)

buttonaddlines=Button(root, text='ADD', command=addlinessamplelist)
buttonaddlines.grid(row=1,column=6,columnspan=1,sticky=W)

clock = Label(root, anchor=E, font=('times', 10, 'bold'), fg='white',bg='darkgreen')
clock.grid(row=1,column=8,columnspan=2,sticky=[N,S,E,W])

#f=Frame(root,height=1, width=450, bg="grey")
#f.grid(row=2,column=0, columnspan=10, pady=5,sticky=S)

statuslabel=Label(root, text="Program not started")
statuslabel.grid(row=3,column=1, columnspan=9, sticky=W)

nextlabel=Label(root, text="Settings are at the top of the python script")
nextlabel.grid(row=4,column=1, columnspan=9, sticky=W)

timeleftlabel=Label(root, text="                ")
timeleftlabel.grid(row=5,column=1, columnspan=9, sticky=W)

f1=Frame(root,height=1,width=450,bg="grey")
f1.grid(row=10,column=0, columnspan=10, pady=5)

#f1=Frame(root,height=1,width=450,bg="grey")
#f1.grid(row=100,column=0, columnspan=10, pady=5)
#____________________________OPTIONS______________________________________________________
# optionstitle = Label(root, anchor=W, font=('times', 12, 'bold'), text="options:")
# optionstitle.grid(row=10,column=0, columnspan=3, sticky=[N,S,E,W])

#f2=Frame(root,height=1,width=450,bg="grey")
#f2.grid(row=120,column=0, columnspan=10, pady=5)

#_________________________ERRORS/WARNINGS____________________________________________________
errorlabel = Label(root, anchor=W, font=('times', 12, 'bold'), text="no errors detected")
errorlabel.grid(row=20,column=0, columnspan=10, sticky=[N,S,E,W])

def tick():
    clock.config(text=time.strftime('%H:%M:%S'))
    clock.after(200, tick)
    
tick()
root.mainloop()



