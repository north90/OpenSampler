#-------------------- NOTES--------------------------------------------------
# program by Frank Krijnen
# tested on Windows XP & 7
# needs Python (2.7) and pyserial

#----------------------------------------------------------------------------
#__________________ USER SETTINGS____________________________________________
#----------------------------------------------------------------------------

# COMMUNICATION SETTINGS
# comport to which the OpenSampler is attached (1) look this up in "device manager" look for Arduino  Mega
comport_opensampler=13

# baudrate to OpenSampler (115200)
baudrate_opensampler=115200

# amount sample positions
amount_positions=120

# x position of first tube
xoffset=24.0
# y position of first tube
yoffset=0.5

# X positions in mm, measured from xhome+xoffset (=x position of first tube)
xmm=[0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,0,19,38,57,76,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,109,128,147,166,185,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294,218,237,256,275,294]
# Y positions in mm, measured from yhome+yoffset (=y position of first tube)
ymm=[0,0,0,0,0,19,19,19,19,19,38,38,38,38,38,57,57,57,57,57,76,76,76,76,76,95,95,95,95,95,114,114,114,114,114,133,133,133,133,133,0,0,0,0,0,19,19,19,19,19,38,38,38,38,38,57,57,57,57,57,76,76,76,76,76,95,95,95,95,95,114,114,114,114,114,133,133,133,133,133,0,0,0,0,0,19,19,19,19,19,38,38,38,38,38,57,57,57,57,57,76,76,76,76,76,95,95,95,95,95,114,114,114,114,114,133,133,133,133,133]


zUp=0
zDown=30
zLen=80

# message to turn on flushing 
flushing_on=('M106')
flushing_off=('M107')

# message to turn on LED BACKLIGHT 
backlight_on=('M206 S255.0')
backlight_off=('M206 S0.0')
backlight2_on=('M306 S255.0')
backlight2_off=('M306 S0.0')

# message to turn off motors
motors_off=('M84')

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

# create a root TkInter frame
root = Tk()
root.title('Manual OpenSampler controller v20151006')

comerror=0
OpenSamplerSer = serial.Serial(comport_opensampler-1, baudrate_opensampler, timeout=2)  
#sleep 2 seconds after opening port to controller so it can reboot
# the serial has to be kept open otherwise it resets
time.sleep(2)   

#-----------------------------------------------------------------------------------------
#____________________________ VARIABLES_______________________________________________
#--------------------------------------------------------------------------------------
ishomed=0

#---------------------------------------------------------------------------------------------
#____________________ MAIN routine______________________________________________________________
#----------------------------------------------------------------------------------------------
# isn't there because this is manual control

#---------------------------------------------------------------------------------------------
#____________________ Sub routines______________________________________________________________
#----------------------------------------------------------------------------------------------
  
def serial2OpenSampler(data2send):
   #sys.stdout.write("send selector1: " + data2send )
   print "sending to OpenSampler: " + data2send 
   try:
      OpenSamplerSer.write(data2send+'\r')
      print "succes"      
   except:
      errorlabel.config(text="ERROR: COULD NOT SEND SERIAL DATA")  

def GoHome():
   global ishomed
   serial2OpenSampler("G28")
   ishomed=1
   
def GoPosition():
   gotopos=int(sampleposentry.get())
   if (gotopos > 0 and gotopos < amount_positions+1 ):
      GoZ(zUp)
      GoXYZ(xoffset+xmm[gotopos-1],yoffset+ymm[gotopos-1],zUp)

def testGoZ():
   gotoz=int(gozentry.get())
   if (gotoz > -1 and gotoz < zLen+1 ):
      GoZ(gotoz)
      
      
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
   serial2OpenSampler(flushing_on)

def FlushingOff():
   serial2OpenSampler(flushing_off)  

def BackLightOn():
   serial2OpenSampler(backlight_on)

def BackLightOff():
   serial2OpenSampler(backlight_off) 
   
def BackLight2On():
   serial2OpenSampler(backlight2_on)

def BackLight2Off():
   serial2OpenSampler(backlight2_off) 
   
def MotorsOff():
    serial2OpenSampler(motors_off) 

# -------------------------------------------------------------------------------------------------
#___________________ START OF GUI_________________________________________

logo=Label(root, anchor=W, bg='darkgreen')
clock = Label(root, anchor=E, font=('times', 20, 'bold'), fg='white',bg='darkgreen')
logo.grid(row=0,column=0,columnspan=17,sticky=[N,S,E,W])
clock.grid(row=0,column=8,columnspan=8,sticky=[N,S,E,W])
   
f=Frame(root,height=1, width=450, bg="grey")
f.grid(row=2,column=0, columnspan=10, pady=5,sticky=S)

statuslabel=Label(root, text="Test OpenSampler")
statuslabel.grid(row=3,column=1, columnspan=9, sticky=W)

f1=Frame(root,height=1,width=450,bg="grey")
f1.grid(row=10,column=0, columnspan=10, pady=5)

#____________________________OPTIONS______________________________________________________
optionstitle = Label(root, anchor=W, font=('times', 12, 'bold'), text="options:")
optionstitle.grid(row=11,column=0, columnspan=3, sticky=[N,S,E,W])

gohomelabel = Label(root, text="Move OpenSampler home")
gohomelabel.grid(row=12,column=0, columnspan=7, sticky=W)
gohomeapply = Button(root, text="GO HOME", command=GoHome)
gohomeapply.grid(row=12,column=6, columnspan=5, sticky=W)

gosamplelabel = Label(root, text="Move OpenSampler to position")
gosamplelabel .grid(row=13,column=0, columnspan=7, sticky=W)
sampleposentry= Entry(root,width=4)
sampleposentry.insert(0,"1")
sampleposentry.grid(row=14,column=1, columnspan=1, sticky=[W])
gosampleapply = Button(root, text="GO", command=GoPosition)
gosampleapply.grid(row=14,column=6, columnspan=5, sticky=W)

gozlabel = Label(root, text="Move needle to")
gozlabel .grid(row=15,column=0, columnspan=7, sticky=W)
gozentry= Entry(root,width=4)
gozentry.insert(0,"0")
gozentry.grid(row=16,column=1, columnspan=1, sticky=[W])
gozapply = Button(root, text="GO", command=testGoZ)
gozapply.grid(row=17,column=6, columnspan=5, sticky=W)

flushlabel = Label(root, text="Flushing solenoid")
flushlabel.grid(row=18,column=0, columnspan=7, sticky=W)
flushingonapply = Button(root, text="Flush ON", command=FlushingOn)
flushingonapply.grid(row=18,column=6, columnspan=5, sticky=W)
flushingoffapply = Button(root, text="Flush OFF", command=FlushingOff)
flushingoffapply.grid(row=19,column=6, columnspan=5, sticky=W)

backlightlabel = Label(root, text="BackLight")
backlightlabel.grid(row=20,column=0, columnspan=7, sticky=W)
backlightonapply = Button(root, text="BackLight ON", command=BackLightOn)
backlightonapply.grid(row=20,column=6, columnspan=5, sticky=W)
backlightoffapply = Button(root, text="BackLight OFF", command=BackLightOff)
backlightoffapply.grid(row=21,column=6, columnspan=5, sticky=W)

backlightlabel = Label(root, text="BackLight2")
backlightlabel.grid(row=22,column=0, columnspan=7, sticky=W)
backlightonapply = Button(root, text="BackLight2 ON", command=BackLight2On)
backlightonapply.grid(row=22,column=6, columnspan=5, sticky=W)
backlightoffapply = Button(root, text="BackLight2 OFF", command=BackLight2Off)
backlightoffapply.grid(row=23,column=6, columnspan=5, sticky=W)

motorslabel = Label(root, text="Motors")
motorslabel.grid(row=28,column=0, columnspan=7, sticky=W)
motorsoffapply = Button(root, text="Motors OFF", command=MotorsOff)
motorsoffapply.grid(row=29,column=6, columnspan=5, sticky=W)

f2=Frame(root,height=1,width=450,bg="grey")
f2.grid(row=30,column=0, columnspan=10, pady=5)

#_________________________ERRORS/WARNINGS____________________________________________________
errorlabel = Label(root, anchor=W, font=('times', 12, 'bold'), text="no errors detected")
errorlabel.grid(row=31,column=0, columnspan=10, sticky=[N,S,E,W])

def tick():
   global timelastsolenoidrefresh
   clock.config(text=time.strftime('%H:%M:%S'))
   clock.after(200, tick)
    
tick()
root.mainloop()



