from Tkinter import *
import tkFileDialog
import tkMessageBox

import os
import string
import time
import datetime
import csv
import numpy
import calendar
from scipy import stats
from scipy import optimize
from scipy import linspace
import math
import pylab as P
from matplotlib.backends.backend_pdf import PdfPages
import fnmatch

#confidence interval for linear regression analysis
confidence_interval=90.0

def MergeResults():
   global sampletimefilename
   global mergedresultsfilename
   global tempfilename
   
   inputfoldername = 'C:\UserData'
   resultsfoldername = 'C:\DATA_TOOLS_UOFS'
   
   opensampletimefile=open(sampletimefilename, 'rb')
   sampletimes = numpy.genfromtxt(opensampletimefile, delimiter=',', dtype=None, names=True)
   
   sampleepochtimes=[]; 
   c1=0
   # run through sampletimefile and find first and last date
   for row in sampletimes['SampleName']:
      samplestartstr=str(sampletimes['Year'][c1])+" "+str(sampletimes['Month'][c1])+" "+str(sampletimes['Day'][c1])+" "+str(sampletimes['Hour'][c1])+" "+str(sampletimes['Minute'][c1]) +" "+str(sampletimes['Second'][c1])
      samplestructtime=time.strptime(samplestartstr, "%Y %m %d %H %M %S")
      sampleepochtime=calendar.timegm(samplestructtime)
      sampleepochtimes.append(sampleepochtime)
      c1=c1+1
   
   sampleepochtimes=sorted(sampleepochtimes)
   firstsampletime=min(sampleepochtimes)
   lastsampletime=max(sampleepochtimes)  
   print sampleepochtimes
       
   os.chdir(resultsfoldername)
   mergedresultsfilename=datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '_merged_results.txt'
   openresultsfile=open(mergedresultsfilename, 'wb')
   resultswriter = csv.writer(openresultsfile, delimiter='\t')
   #[fd['DATE'][c1],fd['TIME'][c1],fd['EPOCH_TIME'][c1],fd['N2O'][c1],fd['d15N'][c1],fd['d15Nalpha'][c1],fd['d15Nbeta'][c1],fd['co2_conc'][c1],fd['H2O_conc'][c1])
   resultswriter.writerow(['Date','Local_Time','Epoch_Time','12CO2_ppmv','13CO2_ppmv', 'd13C', 'H2O_volperc'])
 
   os.chdir(inputfoldername)
      
   for dirpath, dirs, files in os.walk(inputfoldername):
      for filename in fnmatch.filter(files, '*Data.dat'):
         openinputfile=open(os.path.join(dirpath, filename),'rb')
         junk,datestr,junk2=filename.split("-",2)
         YMD=int(datestr)
         yearoffile=YMD/10000
         monthoffile=(YMD-yearoffile*10000)/100
         dayoffile=YMD-yearoffile*10000-monthoffile*100
         
         filetimestr=str(yearoffile)+" "+str(monthoffile)+" "+str(dayoffile)+" 00 00 00"
         filestructtime=time.strptime(filetimestr, "%Y %m %d %H %M %S")
         fileepochtime=calendar.timegm(filestructtime)
         
         if fileepochtime > firstsampletime-86400 and fileepochtime < lastsampletime+86400:
            print filename
            print datestr
            fd = numpy.genfromtxt(openinputfile, dtype=None, names=True)
            c1=0
            for row in fd['TIME']:
               temptime,junk=row.split(".",1)
               datetimestr=str(fd['DATE'][c1])+" "+str(temptime)
               tempstructtime=time.strptime(datetimestr, "%m/%d/%y %H:%M:%S")
               tempepochtime=time.mktime(tempstructtime)
               tempepochtime=tempepochtime
               tempstructtime=time.localtime(tempepochtime)
               
               gooddate=time.strftime("%Y-%m-%d", tempstructtime)
               goodtime=(time.strftime("%H:%M:%S", tempstructtime))

               resultswriter.writerow([gooddate,goodtime,tempepochtime+(int(UTCoffsetentry.get())*3600),fd['12CO2'][c1],fd['13CO2_Raw'][c1],fd['Delta_Raw'][c1],fd['H2O'][c1]])
               c1=c1+1      
         openinputfile.close()
         
   openresultsfile.close()
   
def askopenresultsfilename():
   global sampletimefilename  # file with the sample names and times (switcherlog)
   global mergedresultsfilename
   global tempfilename
      
   # get filename
   fileopen_opt = options = {}
   options['defaultextension'] = '.csv' 
   options['filetypes'] = [('csv files', '.csv'),('all files', '.*')]
   options['initialdir'] = 'C:\SWITCH_CONTROL\SWITCHERLOG'
   options['initialfile'] = 'sample_times_names.csv'
   options['parent'] = root
   options['title'] = 'Choose a csv file with samplenames and times to open'
   sampletimefilename = tkFileDialog.askopenfilename(**fileopen_opt)

   # open file 
   if sampletimefilename:
      tempfilename=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
      MergeResults()
      
      opensampletimefile=open(sampletimefilename, 'rb')
      resultsfoldername = 'C:\DATA_TOOLS_UOFS'
      os.chdir(resultsfoldername)
      openinputfile=open(mergedresultsfilename, 'rb')
      resultsfileName=tempfilename + '_results.csv'
      openresultsfile=open(resultsfileName, 'wb')
      
      pdffile1 = PdfPages(tempfilename +'_charts_sample_only.pdf')
      pdffile2 = PdfPages(tempfilename +'_charts_whole_run.pdf')

      sampletimes = numpy.genfromtxt(opensampletimefile, delimiter=',', dtype=None, names=True)
      print "amount samples"      
      print len(sampletimes['SampleName'])
      
      iCO2data = numpy.genfromtxt(openinputfile, delimiter='\t', dtype=None, names=True)
      print "amount datalines"    
      print len(iCO2data['Epoch_Time'])
      amountrows=len(iCO2data['Epoch_Time'])
      
      quality='unknown'
      
      resultswriter = csv.writer(openresultsfile, dialect='excel')
      resultswriter.writerow(['SampleName', 'Rundate','Runtime', 'Port', 'Quality', '12CO2mean', '12CO2slope', '12CO2intercept',
      '13CO2mean','13CO2slope','13CO2intercept', 'd13Cmean', 'd13Cslope', 'd13Cintercept','H2Omean'])
      stabilizesec=float(pretimeentry.get())
      sampletimesec=float(sampletimeentry.get())*60         
      
      # just a counter c1 for keeping track of where we are in the samplelist file
      c1=0 
      # just a counter c2 for keeping track of where we are in the results file
      c2=0
      
      
      for row in sampletimes['SampleName']:
         xsec=[]; y12CO2=[]; y13CO2=[]; yd13C=[]; yH2O=[];
         xsecs=[]; y12CO2s=[]; y13CO2s=[]; yd13Cs=[]; yH2Os=[];
         samplestartstr=str(sampletimes['Year'][c1])+" "+str(sampletimes['Month'][c1])+" "+str(sampletimes['Day'][c1])+" "+str(sampletimes['Hour'][c1])+" "+str(sampletimes['Minute'][c1]) +" "+str(sampletimes['Second'][c1])
         samplestructtime=time.strptime(samplestartstr, "%Y %m %d %H %M %S")
         sampleepochtime=calendar.timegm(samplestructtime)
         print sampletimes['SampleName'][c1]
         print time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)
         print sampleepochtime
         # discard data before sample is started and stabilized
         while sampleepochtime > iCO2data['Epoch_Time'][c2]:
            c2=c2+1 
         while sampleepochtime+stabilizesec > iCO2data['Epoch_Time'][c2]:
            xsec.append(iCO2data['Epoch_Time'][c2]-sampleepochtime)
            y12CO2.append(iCO2data['12CO2_ppmv'][c2])
            y13CO2.append(iCO2data['13CO2_ppmv'][c2])
            yd13C.append(iCO2data['d13C'][c2])
            yH2O.append(iCO2data['H2O_volperc'][c2])
            c2=c2+1            
         while sampleepochtime+stabilizesec+sampletimesec > iCO2data['Epoch_Time'][c2]:
            xsecs.append(iCO2data['Epoch_Time'][c2]-sampleepochtime)
            y12CO2s.append(iCO2data['12CO2_ppmv'][c2])
            y13CO2s.append(iCO2data['13CO2_ppmv'][c2])
            yd13Cs.append(iCO2data['d13C'][c2])
            yH2Os.append(iCO2data['H2O_volperc'][c2])
            c2=c2+1
         while sampleepochtime+stabilizesec+sampletimesec+120 > iCO2data['Epoch_Time'][c2]:
            xsec.append(iCO2data['Epoch_Time'][c2]-sampleepochtime)
            y12CO2.append(iCO2data['12CO2_ppmv'][c2])
            y13CO2.append(iCO2data['13CO2_ppmv'][c2])
            yd13C.append(iCO2data['d13C'][c2])
            yH2O.append(iCO2data['H2O_volperc'][c2])
            c2=c2+1   
         c2=0
         print 'amount readings for this sample:' + str(len(y12CO2s))
         rundate=time.strftime("%Y%m%d", samplestructtime)
         runtime=time.strftime("%H%M%S", samplestructtime)
         
         if len(y12CO2s)>2:
            _12CO2mean=numpy.mean(y12CO2s)
            _13CO2mean=numpy.mean(y13CO2s)
            d13Cmean=numpy.mean(yd13Cs)
            H2Omean=numpy.mean(yH2Os)
            
            if _12CO2mean > 1500:
               quality='CO2 high'
            elif _12CO2mean < 300:
               quality='CO2 low'
            else:
               quality=''
            if _13CO2mean > 25:
               quality=quality + ' 13CO2 high'
            elif _13CO2mean < 3:   
               quality=quality + ' 13CO2 low'
            if H2Omean > 3 :
               quality= quality + ' H2O too high, DAMAGE POSSIBLE!'
            elif H2Omean > 1 :
               quality= quality + ' H2O high'
                       
            _12CO2slope, _12CO2intercept, _12CO2linr, _12CO2linp, _12CO2std_err = stats.linregress(xsecs,y12CO2s)
            _13CO2slope, _13CO2intercept, _13CO2linr, _13CO2linp, _13CO2std_err = stats.linregress(xsecs,y13CO2s)
            d13Cslope, d13Cintercept, d13Clinr, d13Clinp, d13Cstd_err = stats.linregress(xsecs,yd13Cs)
            
            
            
            
            resultswriter.writerow([sampletimes['SampleName'][c1],rundate,runtime, sampletimes['Port'][c1], 
            quality, _12CO2mean, _12CO2slope, _12CO2intercept, _13CO2mean, _13CO2slope, _13CO2intercept,
            d13Cmean, d13Cslope, d13Cintercept, H2Omean])
      
            # # save fluxes to file
            xs = numpy.array(xsecs)            
            y1s = numpy.array(y12CO2s)
            y2s = numpy.array(y13CO2s)
            y3s = numpy.array(yd13Cs)
            
            x = numpy.array(xsec)            
            y1 = numpy.array(y12CO2)
            y2 = numpy.array(y13CO2)
            y3 = numpy.array(yd13C)
            
            #____________________________ SAMPLE ONLY PDF______________________________
            fig = P.figure(figsize=(16, 16))
            (m,b)=P.polyfit(xs,y1s,1)
            y12 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y2s,1)
            y22 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y3s,1)
            y32 = P.polyval([m,b],x)
                
            line1=fig.add_subplot(311)
            line1.scatter(xs, y1s)
            line1.set_xlim(left=0)         
            line1.grid()
            line1.set_title('Sample Name: '+str(sampletimes['SampleName'][c1])+'        time:  '+time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)) 
            line1.set_ylabel('12CO2 concentration (ppmv)', color='b')
            
            line2=fig.add_subplot(312)
            line2.scatter(xs, y2s)
            line2.set_xlim(left=0)
            line2.grid() 
            line2.set_ylabel('13CO2 concentration (ppmv)', color='b')
                              
            line3=fig.add_subplot(313)
            line3.scatter(xs, y3s)
            line3.set_xlim(left=0)
            line3.grid()
            line3.set_ylabel('d13C permil', color='b')
            line3.set_xlabel('time (seconds)', color='b')
            
            pdffile1.savefig(dpi=150)
            P.close()

            #_____________________ whole run PDF___________________________________________
            fig = P.figure(figsize=(16, 16))
            (m,b)=P.polyfit(xs,y1s,1)
            y12 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y2s,1)
            y22 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y3s,1)
            y32 = P.polyval([m,b],x)
                
            line1=fig.add_subplot(311)
            line1.scatter(xs, y1s)
            line1.scatter(x, y1, marker='+')
            line1.set_xlim(left=0)         
            line1.grid()
            line1.set_title('Sample Name: '+str(sampletimes['SampleName'][c1])+'        time:  '+time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)) 
            line1.set_ylabel('12CO2 concentration (ppmv)', color='b')
            
            line2=fig.add_subplot(312)
            line2.scatter(xs, y2s)
            line2.scatter(x, y2, marker='+')
            line2.set_xlim(left=0)
            line2.grid() 
            line2.set_ylabel('13CO2 concentration (ppmv)', color='b')
                              
            line3=fig.add_subplot(313)
            line3.scatter(xs, y3s)
            line3.scatter(x, y3, marker='+')
            line3.set_xlim(left=0)
            line3.grid()
            line3.set_ylabel('d13C permil', color='b')
            line3.set_xlabel('time (seconds)', color='b')
            
            pdffile2.savefig(dpi=150)
            P.close() 
            
         else:
            resultswriter.writerow([sampletimes['SampleName'][c1],rundate,runtime, sampletimes['Port'][c1],
               'na', 'na', 'na', 'na','na','na',
               'na', 'na', 'na', 'na'])
            print 'NO DATA FOUND FOR THIS SAMPLE'
         print '----------------------------------------------'   
         c1=c1+1
      
      openinputfile.close()
      openresultsfile.close()
      pdffile1.close()
      pdffile2.close()


#____________________________________________________________________________________________________________
#--------------------GUI-----------------------------------------------------------------------------------
#_____________________________________________________________________________________________________________

# create a root TkInter frame
root = Tk()
root.title('iCO2 results calculator 20130715')

#__________________________________LOGO&TITLE________________________________________

bigtitle = Label(root, anchor=W, font=('times', 20, 'bold'), fg='white',bg='darkgreen', text="iCO2 calculator ")
bigtitle.grid(row=0,column=0,columnspan=10,sticky=[N,S,E,W])

#____________________________OPTIONS______________________________________________________
optionstitle = Label(root, anchor=W, font=('times', 12, 'bold'), text="options:")
optionstitle.grid(row=1,column=0, columnspan=3, sticky=[N,S,E,W])


pretimeentrytitle = Label(root, anchor=W, text="stabilizing time to ignore at start (s):")
pretimeentrytitle.grid(row=3,column=0, columnspan=1, sticky=[E])
pretimeentry= Entry(root,width=4)
pretimeentry.insert(0,"270")
pretimeentry.grid(row=3,column=1, columnspan=1, sticky=[W])

sampletimeentrytitle = Label(root, anchor=W, text="sampling time to include (min):")
sampletimeentrytitle.grid(row=4,column=0, columnspan=1, sticky=[E])
sampletimeentry= Entry(root,width=4)
sampletimeentry.insert(0,"5")
sampletimeentry.grid(row=4,column=1, columnspan=1, sticky=[W])

UTCoffsettitle = Label(root, anchor=W, text="Offset local time UTC (SK: -6):")
UTCoffsettitle.grid(row=13,column=0, columnspan=1, sticky=[E])
UTCoffsetentry= Entry(root,width=4)
UTCoffsetentry.insert(0,"-6")
UTCoffsetentry.grid(row=13,column=1, columnspan=1, sticky=[W])

# doHMRfit=IntVar()
# doHMRapply = Checkbutton(root, text="Fit the exponential HMR model", variable=doHMRfit)
# doHMRapply.grid(row=12,column=0, columnspan=5, sticky=W)

# _______________________CALC INDIVIDUAL FLUXES_____________________________________________
f0=Frame(root,height=1, width=450, bg="grey")
f0.grid(row=24,column=0, columnspan=4, pady=5,sticky=S)

calcfluxtitle = Label(root, anchor=W, font=('times', 12, 'bold'), text="Calculate results")
calcfluxtitle.grid(row=25,column=0, columnspan=4, sticky=[N,S,E,W])
calcfluxhelp = Label(root, anchor=W, text="Open a merged results file")
calcfluxhelp.grid(row=26,column=0, columnspan=4, sticky=[N,S,E,W])
calcfluxhelp2 = Label(root, anchor=W, text="input concentrations in ppmv (=ul/l)")
calcfluxhelp2.grid(row=27,column=0, columnspan=4, sticky=[N,S,E,W])

buttonopenconcfile=Button(root, text='open sampletime and results file', command=askopenresultsfilename)
buttonopenconcfile.grid(row=28,column=1,columnspan=1,sticky=[W])
calcfluxhelp3 = Label(root, anchor=W, text="results are saved with same filename+results")
calcfluxhelp3.grid(row=29,column=0, columnspan=4, sticky=[N,S,E,W])

# #_____________________________________________________________________________________________________________

root.mainloop(  )



