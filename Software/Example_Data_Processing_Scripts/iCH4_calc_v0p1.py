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

#resultsfoldername='C:\UserData'
resultsfoldername = 'C:\DATA_TOOLS_UOFS'

def MergeResults():
   global sampletimefilename
   global mergedresultsfilename
   global tempfilename
   
   inputfoldername = 'C:\UserData'
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

   resultswriter.writerow(['Date','Local_Time','Epoch_Time','HP_12CH4','HP_13CH4', 
   'HP_Delta_iCH4_Raw', '12CO2','13CO2','Delta_Raw_iCO2', 'H2O', 'ChemDetect'])
   os.chdir(inputfoldername)
      
   for dirpath, dirs, files in os.walk(inputfoldername):
      for filename in fnmatch.filter(files, '*.dat'):
         openinputfile=open(os.path.join(dirpath, filename),'rb')
         print filename
         junk,datestr,junk2=filename.split("-",2)
         #print datestr
         YMD=int(datestr)
         yearoffile=YMD/10000
         monthoffile=(YMD-yearoffile*10000)/100
         dayoffile=YMD-yearoffile*10000-monthoffile*100
         
         filetimestr=str(yearoffile)+" "+str(monthoffile)+" "+str(dayoffile)+" 00 00 00"
         filestructtime=time.strptime(filetimestr, "%Y %m %d %H %M %S")
         fileepochtime=calendar.timegm(filestructtime)
         
         if fileepochtime > firstsampletime-86400 and fileepochtime < lastsampletime+86400:
            try:
               fd = numpy.genfromtxt(openinputfile, dtype=None, names=True)
               c1=0
               for row in fd['TIME']:
                  temptime,junk=row.split(".",1)
                  datetimestr=str(fd['DATE'][c1])+" "+str(temptime)
                  tempstructtime=time.strptime(datetimestr, "%Y-%m-%d %H:%M:%S")
                  tempepochtime=time.mktime(tempstructtime)
                  tempepochtime=tempepochtime+(int(UTCoffsetentry.get())*3600)
                  tempstructtime=time.localtime(tempepochtime)
                  
                  gooddate=time.strftime("%Y-%m-%d", tempstructtime)
                  goodtime=(time.strftime("%H:%M:%S", tempstructtime))

                  resultswriter.writerow([gooddate,goodtime,fd['EPOCH_TIME'][c1],fd['HP_12CH4'][c1],fd['HP_13CH4'][c1],
                  fd['HP_Delta_iCH4_Raw'][c1],fd['12CO2'][c1],fd['13CO2'][c1],fd['Delta_Raw_iCO2'][c1],
                  fd['H2O'][c1],fd['ChemDetect'][c1]])
                  c1=c1+1
            except:
               print "could not read: " + filename
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
   options['initialdir'] = 'C:\UserDataiCH4\SAMPLELOG'
   options['initialfile'] = 'sample_times_names.csv'
   options['parent'] = root
   options['title'] = 'Choose a csv file with samplenames and times to open'
   sampletimefilename = tkFileDialog.askopenfilename(**fileopen_opt)

   # open file 
   if sampletimefilename:
      tempfilename=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
      MergeResults()
      
      opensampletimefile=open(sampletimefilename, 'rb')
      os.chdir(resultsfoldername)
      openinputfile=open(mergedresultsfilename, 'rb')
      resultsfileName=tempfilename + '_results.csv'
      openresultsfile=open(resultsfileName, 'wb')
      
      pdffile1 = PdfPages(tempfilename +'_charts_sample_only.pdf')
      pdffile2 = PdfPages(tempfilename +'_charts_whole_run.pdf')

      sampletimes = numpy.genfromtxt(opensampletimefile, delimiter=',', dtype=None, names=True)
      print "amount samples"      
      print len(sampletimes['SampleName'])
      
      iCH4data = numpy.genfromtxt(openinputfile, delimiter='\t', dtype=None, names=True)
      print "amount datalines"    
      print len(iCH4data['Epoch_Time'])
      amountrows=len(iCH4data['Epoch_Time'])
      
      resultswriter = csv.writer(openresultsfile, dialect='excel')
      resultswriter.writerow(['SampleName', 'Rundate','Runtime', 'Port', '12CH4mean', 
      '12CH4slope', '12CH4intercept','12CH4mean','13CH4slope','13CH4intercept', 'd13C_CH4mean',
      'd13C_CH4slope', 'd13C_CH4intercept','12CO2mean', '12CO2slope', '12CO2intercept',
      '13CO2mean', '13CO2slope','13CO2intercept', 'd13C_CO2mean', 'd13C_CO2slope','d13C_CO2intercept',
      'H2Omean','ChemDetect'])
      stabilizesec=float(pretimeentry.get())
      sampletimesec=float(sampletimeentry.get())*60        
      
      # just a counter c1 for keeping track of where we are in the samplelist file
      c1=0 
      # just a counter c2 for keeping track of where we are in the results file
      c2=0
      
      for row in sampletimes['SampleName']:
         xsec=[]; y12CH4=[]; y13CH4=[]; yd13CCH4=[]; y12CO2=[]; y13CO2=[]; yd13CC02=[]; yH2O=[]; yChemDetect=[];
         xsecs=[]; y12CH4s=[]; y13CH4s=[]; yd13CCH4s=[]; y12CO2s=[]; y13CO2s=[]; yd13CCO2s=[]; yH2Os=[]; yChemDetects=[];
         
         samplestartstr=str(sampletimes['Year'][c1])+" "+str(sampletimes['Month'][c1])+" "+str(sampletimes['Day'][c1])+" "+str(sampletimes['Hour'][c1])+" "+str(sampletimes['Minute'][c1]) +" "+str(sampletimes['Second'][c1])
         samplestructtime=time.strptime(samplestartstr, "%Y %m %d %H %M %S")
         #sampleepochtime=time.mktime(samplestructtime)
         sampleepochtime=calendar.timegm(samplestructtime)
         sampleepochtime=sampleepochtime-(int(UTCoffsetentry.get())*3600)
         print sampletimes['SampleName'][c1]
         print time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)
         print sampleepochtime
         # discard data before sample is started and stabilized
         while sampleepochtime > iCH4data['Epoch_Time'][c2]:
            c2=c2+1 
         while sampleepochtime+stabilizesec > iCH4data['Epoch_Time'][c2]:
            xsec.append(iCH4data['Epoch_Time'][c2]-sampleepochtime)
            y12CH4.append(iCH4data['HP_12CH4'][c2])
            y13CH4.append(iCH4data['HP_13CH4'][c2])
            yd13CCH4.append(iCH4data['HP_Delta_iCH4_Raw'][c2])
            y12CO2.append(iCH4data['12CO2'][c2])
            y13CO2.append(iCH4data['13CO2'][c2])
            yd13CC02.append(iCH4data['Delta_Raw_iCO2'][c2])
            yH2O.append(iCH4data['H2O'][c2])
            yChemDetect.append(iCH4data['ChemDetect'][c2])
            c2=c2+1            
         while sampleepochtime+stabilizesec+sampletimesec > iCH4data['Epoch_Time'][c2]:
            xsecs.append(iCH4data['Epoch_Time'][c2]-sampleepochtime)
            y12CH4s.append(iCH4data['HP_12CH4'][c2])
            y13CH4s.append(iCH4data['HP_13CH4'][c2])
            yd13CCH4s.append(iCH4data['HP_Delta_iCH4_Raw'][c2])
            y12CO2s.append(iCH4data['12CO2'][c2])
            y13CO2s.append(iCH4data['13CO2'][c2])
            yd13CCO2s.append(iCH4data['Delta_Raw_iCO2'][c2])
            yH2Os.append(iCH4data['H2O'][c2])
            yChemDetects.append(iCH4data['ChemDetect'][c2])
            c2=c2+1
         while sampleepochtime+stabilizesec+sampletimesec+120 > iCH4data['Epoch_Time'][c2]:
            xsec.append(iCH4data['Epoch_Time'][c2]-sampleepochtime)
            y12CH4.append(iCH4data['HP_12CH4'][c2])
            y13CH4.append(iCH4data['HP_13CH4'][c2])
            yd13CCH4.append(iCH4data['HP_Delta_iCH4_Raw'][c2])
            y12CO2.append(iCH4data['12CO2'][c2])
            y13CO2.append(iCH4data['13CO2'][c2])
            yd13CC02.append(iCH4data['Delta_Raw_iCO2'][c2])
            yH2O.append(iCH4data['H2O'][c2])
            yChemDetect.append(iCH4data['ChemDetect'][c2])
            c2=c2+1   
         c2=0
         print 'amount readings for this sample:' + str(len(y12CH4s))
         rundate=time.strftime("%Y%m%d", samplestructtime)
         runtime=time.strftime("%H%M%S", samplestructtime)
         
         if len(y12CH4s)>2:
            #xsecs=[]; y12CH4s=[]; y13CH4s=[]; yd13CCH4s=[]; y12CO2s=[]; y13CO2s=[]; yd13CCO2s=[]; yH2Os=[]; yChemDetect
            _12CH4mean=numpy.mean(y12CH4s)
            _13CH4mean=numpy.mean(y13CH4s)
            d13CCH4mean=numpy.mean(yd13CCH4s)
            _12CO2mean=numpy.mean(y12CO2s)
            _13CO2mean=numpy.mean(y13CO2s)
            d13CCO2mean=numpy.mean(yd13CCO2s)
            H2Omean=numpy.mean(yH2Os)
            ChemDetectmean=numpy.mean(yChemDetect)
            
            _12CH4slope, _12CH4intercept, _12CH4linr, _12CH4linp, _12CH4std_err = stats.linregress(xsecs,y12CH4s)
            _13CH4slope, _13CH4intercept, _13CH4linr, _13CH4linp, _13CH4std_err = stats.linregress(xsecs,y13CH4s)
            d13CCH4slope, d13CCH4intercept, d13CCH4linr, d13CCH4linp, d13CCH4std_err = stats.linregress(xsecs,yd13CCH4s)
            _12CO2slope, _12CO2intercept, _12CO2linr, _12CO2linp, _12CO2std_err = stats.linregress(xsecs,y12CO2s)
            _13CO2slope, _13CO2intercept, _13CO2linr, _13CO2linp, _13CO2std_err = stats.linregress(xsecs,y13CO2s)
            d13CCO2slope, d13CCO2intercept, d13CCO2linr, d13CCO2linp, d13CCO2std_err = stats.linregress(xsecs,yd13CCO2s)
          
            resultswriter.writerow([sampletimes['SampleName'][c1],rundate,runtime, sampletimes['Port'][c1],
            _12CH4mean, _12CH4slope, _12CH4intercept, _13CH4mean, _13CH4slope, _13CH4intercept, 
            d13CCH4mean, d13CCH4slope, d13CCH4intercept, _12CO2mean, _12CO2slope, _12CO2intercept,
            _13CO2mean, _13CO2slope,_13CO2intercept,d13CCO2mean,d13CCO2slope,d13CCO2intercept,H2Omean,ChemDetectmean])
                     
            #______________ SAMPLE ONLY PDF_______________________________
            fig = P.figure(figsize=(16, 16))
            xs = numpy.array(xsecs)            
            y1s = numpy.array(y12CH4s)
            y2s = numpy.array(yd13CCH4s)
            y3s = numpy.array(y12CO2s)
            y4s = numpy.array(yd13CCO2s)
            
            x = numpy.array(xsec)            
            y1 = numpy.array(y12CH4)
            y2 = numpy.array(yd13CCH4)
            y3 = numpy.array(y12CO2)
            y4 = numpy.array(yd13CC02)
            (m,b)=P.polyfit(xs,y1s,1)
            y12 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y2s,1)
            y22 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y3s,1)
            y32 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y4s,1)
            y42 = P.polyval([m,b],x)
            
            line1=fig.add_subplot(411)
            line1.scatter(xs, y1s)
            line1.set_xlim(left=0)       
            line1.grid()
            line1.set_title('Sample Name: '+str(sampletimes['SampleName'][c1])+'        time:  '+time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)) 
            line1.set_ylabel('12CH4 concentration (ppmv)', color='b')
            
            line2=fig.add_subplot(412)
            line2.scatter(xs, y2s)
            line2.set_xlim(left=0)
            line2.grid() 
            line2.set_ylabel('d13C CH4 (permil)', color='b')
                              
            line3=fig.add_subplot(413)
            line3.scatter(xs, y3s)
            line3.set_xlim(left=0)
            line3.grid()
            line3.set_ylabel('12CO2 concentration (ppmv)', color='b')
            
            line4=fig.add_subplot(414)
            line4.scatter(xs, y4s)
            line4.set_xlim(left=0)

            line4.grid()
            line4.set_ylabel('d13C CO2 (permil)', color='b')
            line4.set_xlabel('time (seconds)', color='b')
            pdffile1.savefig(dpi=150)
            P.close()
            
            
            #________________________ WHOLE RUN PDF_______________________________
            fig = P.figure(figsize=(16, 16))
            xs = numpy.array(xsecs)            
            y1s = numpy.array(y12CH4s)
            y2s = numpy.array(yd13CCH4s)
            y3s = numpy.array(y12CO2s)
            y4s = numpy.array(yd13CCO2s)
            
            x = numpy.array(xsec)            
            y1 = numpy.array(y12CH4)
            y2 = numpy.array(yd13CCH4)
            y3 = numpy.array(y12CO2)
            y4 = numpy.array(yd13CC02)
            (m,b)=P.polyfit(xs,y1s,1)
            y12 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y2s,1)
            y22 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y3s,1)
            y32 = P.polyval([m,b],x)
            (m,b)=P.polyfit(xs,y4s,1)
            y42 = P.polyval([m,b],x)
            
            line1=fig.add_subplot(411)
            line1.scatter(xs, y1s)
            line1.scatter(x, y1, marker='+')
            line1.set_xlim(left=0)         
            line1.grid()
            line1.set_title('Sample Name: '+str(sampletimes['SampleName'][c1])+'        time:  '+time.strftime("%d %b %Y %H:%M:%S ", samplestructtime)) 
            line1.set_ylabel('12CH4 concentration (ppmv)', color='b')
            
            line2=fig.add_subplot(412)
            line2.scatter(xs, y2s)
            line2.scatter(x, y2, marker='+')
            line2.set_xlim(left=0)
            line2.grid() 
            line2.set_ylabel('d13C CH4 (permil)', color='b')
                              
            line3=fig.add_subplot(413)
            line3.scatter(xs, y3s)
            line3.scatter(x, y3, marker='+')
            line3.set_xlim(left=0)
            line3.grid()
            line3.set_ylabel('12CO2 concentration (ppmv)', color='b')

            line4=fig.add_subplot(414)
            line4.scatter(xs, y4s)
            line4.scatter(x, y4, marker='+')
            line4.set_xlim(left=0)

            line4.grid()
            line4.set_ylabel('d13C CO2 (permil)', color='b')
            line4.set_xlabel('time (seconds)', color='b')
            pdffile2.savefig(dpi=150)
            P.close()
   
         else:
            resultswriter.writerow([sampletimes['SampleName'][c1],rundate,runtime, sampletimes['Port'][c1],
               'na', 'na', 'na', 'na','na',
               'na','na', 'na', 'na', 'na',
               'na', 'na', 'na','na', 'na',
               'na', 'na', 'na','na', 'na'])
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
root.title('iCH4 iCO2 results calculator 20141001')

#__________________________________LOGO&TITLE________________________________________

bigtitle = Label(root, anchor=W, font=('times', 20, 'bold'), fg='white',bg='darkgreen', text="iCH4 & iCO2 calculator ")
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

buttonopenconcfile=Button(root, text='open sampletime file', command=askopenresultsfilename)
buttonopenconcfile.grid(row=28,column=1,columnspan=1,sticky=[W])
calcfluxhelp3 = Label(root, anchor=W, text="results are saved in data_tools_uofs")
calcfluxhelp3.grid(row=29,column=0, columnspan=4, sticky=[N,S,E,W])

# #_____________________________________________________________________________________________________________

root.mainloop(  )



