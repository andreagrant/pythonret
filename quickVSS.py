# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 10:45:22 2012

@author: agrant
"""
#import libraries
#from __future__ import division
from psychopy import visual
from psychopy import gui
from psychopy import core
#from psychopy import data
from psychopy import misc
from psychopy import event
#from psychopy import filters
import time, numpy, random
#import retinotopyScans
#import math
from array import *
import os
#import glob
#import imp
#from Tkinter import *
#from tkFileDialog import askopenfilename
#import psychopy.info

screenNums=[0,1]

if os.path.isfile('lastrun.pickle')==True:
    #found a lastrun file--load scanDict from it
    scanDict=misc.fromFile('lastrun.pickle')
    #scanDict['animFreq']=2
    #scanDict['pairWedge']=1
else:
    #define defaults
    scanDict={
    #Tr (s)
    'Tr':5,
    #number of cycles (traveling wave cycle or stim-rest pairs)
    'numCycles':10,
    #period (s) of each cycle
    'period':24,
    #pre-scan duration (s) --rest before start OR traveling wave to show during throw-away time
    'preScanRest':12,
    #contrast for retinotopy, 0 to 1
    'contrast':1.0,
    #inner radius of stimulus (degrees)
    'innerRadius':0.5,
    #outer radius of stimulus (degrees)
    'outerRadius':12.0,
    #Monitor calibration filename
    #choices are: 7T/AS    3T   7T/PS   debug   other
    'monitor':'other',
    #screen number for operator (normally 0 unless Yedi gets confused)
    'operatorScreen':0,
    #screen number for subject (normally 1)
    'subjectScreen':1,
    #fraction of time the fixation point could change
    'fixFraction':0.2,
    #wedge width for wedges, degrees
    #'wedgeWidth':45,
    #duty cycle for rings, %
    #'dutyCycle':25,
    #animation (drift/flicker) frequency, Hz
    'animFreq':0.2,
    #whether (1) or not (0) to show a second wedge at 180
    'pairWedge':0
    }
#get rid of numScans--it isn't used in dynamic mode
if 'numScans' in scanDict:
    del scanDict['numScans']
#either way, I have the dict. pop a gui
infoDlg=gui.DlgFromDict(dictionary=scanDict,title='Scan parameters',
                        order=['Tr','numCycles','period','preScanRest','contrast','monitor','operatorScreen','subjectScreen','innerRadius','outerRadius','fixFraction','animFreq','pairWedge'],
                        tip={'Tr':'seconds','numCycles':'number of cycles','period':'seconds',
                             'preScanRest':'seconds','contrast':'0 to 1','numScans':'will loop through this many times',
                             'monitor':'choose from 7T/PS, debug, other, 7T/AS',
                             'operatorScreen':'normally 0','subjectScreen':'normallly 1',
                             'innerRadius':'degrees','outerRadius':'degrees',
                             'fixFraction':'fraction of the time the fixation point could change',
                             #'wedgeWidth':'width of wedge (deg) for rotating wedge',
                             #'dutyCycle':'eccentricity width of ring (\%)',
                             'animFreq':'animation frequency, Hz (drift/flicker frequency)',
                             'pairWedge':'draw a second set of wedges on the opposite side (rotating wedges only); 0 o r1 (no/yes)'})
if infoDlg.OK:
    print scanDict
    #running--save the params
    misc.toFile('lastrun.pickle',scanDict)
else:
    print 'user cancelled'
    core.quit()



if '3T' in scanDict['monitor']:
    scanDict['monCalFile'] = 'testMonitor'
elif 'AS' in scanDict['monitor']:
    #monCal = '7TAScaldate'
    #monCal='ASrearProj'
    scanDict['monCalFile']='testMonitor'
elif 'PS' in scanDict['monitor']:
    scanDict['monCalFile']='7TPS'
#    monCal = '7TPS20120921'
elif 'debug' in scanDict['monitor']:
    scanDict['monCalFile']='laptopSelfScreen'
else:
    scanDict['monCalFile']='testMonitor'

if scanDict['operatorScreen']!= scanDict['subjectScreen']:
    if 'AS' in scanDict['monCalFile']:    
        screenSize=[1600,1200]
#        screenSize=[1024,768]
    else:
        screenSize=[1024,768]
else:
    screenSize=[1024,768]




#length of scan in s
scanLength=float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
#open subject window
winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'], 
                   color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=True,allowGUI=False)
winOp = visual.Window([200,200],monitor='testMonitor',units='deg',screen=scanDict['operatorScreen'],
                      color=[0.0,0.0,0.0],colorSpace='rgb')
fixPercentage =scanDict['fixFraction']
fixDuration=0.25
respDuration=1.0
subjectResponse=numpy.zeros((scanLength*60/100,1))
subRespArray=numpy.zeros((scanLength*60/100,3))
subjectResponse[:]=numpy.nan
white=[1.0,1.0,1.0]
gray=[0.0,0.0,0.0]
black=[-1.0,-1.0,-1.0]
IR=scanDict['innerRadius']


#create a designmatrix 
numTrials=240
designMatrix=numpy.zeros((numTrials,3))    

#first N Trs are already zero--rest
#figure out when each stim should be on
#hard code this as ABCBACBCA with 12s rest before/after and between each block
#within each block, show 12 examples drawn randomly from a big list
stimDur=0.75
ISIdur=0.25
trialLength=stimDur+ISIdur
trialsPerBlock=12
blockLength=trialLength*trialsPerBlock
IBIdur=12
#A: 13-24, 109-120, 205-216
#B: 37-48,85-96,157-168
#C: 61-72, 133-144, 181-192
#all others are rest 
designMatrix[12:24,0]=1
designMatrix[36:48,0]=1
designMatrix[64:76,0]=1
designMatrix[96:98,0]=1
designMatrix[120:132,0]=1
designMatrix[144:156,0]=1
designMatrix[168:170,0]=1
designMatrix[192:204,0]=1
designMatrix[216:228,0]=1

stimDur=0.75
ISIdur=0.25

#create the lists with possible stimuli
#letters
#    Alist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
Alist=[u"\u0041",u"\u0042",u"\u0043",u"\u0044",u"\u0045",u"\u0046",u"\u0047",u"\u0048",
        u"\u0049",u"\u004A",u"\u004B",u"\u004C",u"\u004D",u"\u004E",u"\u004F",u"\u0050",
        u"\u0051",u"\u0052",u"\u0053",u"\u0054",u"\u0055",u"\u0056",u"\u0057",u"\u0058",u"\u0059",u"\u005A",
        u"\u0061",u"\u0062",u"\u0063",u"\u0064",u"\u0065",u"\u0066",u"\u0067",u"\u0068",
        u"\u0069",u"\u006A",u"\u006B",u"\u006C",u"\u006D",u"\u006E",u"\u006F",u"\u0070",
        u"\u0071",u"\u0072",u"\u0073",u"\u0074",u"\u0075",u"\u0076",u"\u0077",u"\u0078",u"\u0079",u"\u007A"]
 #wingdings kind of things
Blist=[u"\u2152",u"\u2261",u"\u203B",u"\u00A4",u"\uF0F0",u"\uF0A9",u"\u224C",u"\u3016",u"\u10086",u"\u100B3",u"\u100DD",u"\u1008D",
        u"\u1008F",u"\u100BE",u"\u13A3",u"\u13A8",u"\u13CD",u"\u13DC",u"\u13EB",u"\u13BA",u"\u13EA",u"\u13B9",u"\u13B8",u"\u13C6",
        u"\u13C4",u"\u13F1",u"\u13D1",u"\u13D0",u"\u13E0",u"\u1582",u"\u1596",u"\u1598",u"\u15A7",u"\u155B",u"\u1648",u"\u15D9"]
 #emoticons
Clist=[u"\u1F600",u"\u1F601",u"\u1F602",u"\u1F603",u"\u1F604",u"\u1F605",u"\u1F606",u"\u1F607",u"\u1F608",
           u"\u1F609",u"\u1F60A",u"\u1F60B",u"\u1F60C",u"\u1F60D",u"\u1F60E",u"\u1F60F",u"\u1F610",u"\u1F611",
           u"\u1F612",u"\u1F613",u"\u1F614",u"\u1F615",u"\u1F616",u"\u1F617",u"\u1F618",u"\u1F619",u"\u1F61A",
           u"\u1F61B",u"\u1F61C",u"\u1F61D",u"\u1F61E",u"\u1F61F",u"\u1F620",u"\u1F621",u"\u1F622",u"\u1F623",
           u"\u1F624",u"\u1F625",u"\u1F626",u"\u1F627",u"\u1F628",u"\u1F629",u"\u1F62A",u"\u1F62B",u"\u1F62C",
           u"\u1F62D",u"\u1F62E",u"\u1F62F",u"\u1F630",u"\u1F631",u"\u1F632",u"\u1F633",u"\u1F634",u"\u1F635",
           u"\u1F636",u"\u1F637",u"\u1F638",u"\u1F639",u"\u1F63A",u"\u1F63B",u"\u1F63C",u"\u1F63D",u"\u1F63E",u"\u1F63F"]

#Alist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
#Blist=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','R','U','V','W','X','Y','Z']
#Clist=['1','2','3','4','5','6','7','8','9','0']
numInList=numpy.zeros((3,1))
numInList[0]=len(Alist)
numInList[1]=len(Blist)
numInList[2]=len(Clist)
#generate my random sequence --need 36 of each list
Asequence=numpy.random.randint(0,high=numInList[0],size=36)
Bsequence=numpy.random.randint(0,high=numInList[1],size=36)
Csequence=numpy.random.randint(0,high=numInList[2],size=36)

numpy.savetxt('designMatrix.txt',designMatrix,fmt='%.3i')


#make a fixation cross which will rotate 45 deg on occasion
#this will be a problem. Need a square that embiggens
fix0 = visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
        pos=[8,0],
        fillColor=gray,fillColorSpace='rgb',autoLog=False)
fix1 = visual.ShapeStim(winSub, pos=[8.0,0.0],vertices=((0.0,-0.2),(0.0,0.2)),lineWidth=3.0,
        lineColor=black,lineColorSpace='rgb',
        fillColor=black,fillColorSpace='rgb',autoLog=False)

fix2 = visual.ShapeStim(winSub, pos=[8.0,0.0],vertices=((-0.2,0.0),(0.2,0.0)),lineWidth=3.0,
        lineColor=black,lineColorSpace='rgb',
        fillColor=black,fillColorSpace='rgb',autoLog=False)
 
 
fixOri=0
#create the unicode text stimulus
#    thisText="u"+"\""+Alist[0]+"\""
#    thisText="\""+Alist[0]+"\""

#actualStim=visual.TextStim(winSub,text=Alist[0],color=black,colorSpace='rgb',units='degrees',height=1,pos=(0,0))
actualStim=visual.TextStim(winSub,text=Alist[1],color=[1,1,1],colorSpace='rgb',units='deg',height=2,pos=(2,2))
stim1_v=visual.TextStim(winSub,text='V',color=[1,1,1],colorSpace='rgb',units='deg',height=8,pos=(-8,0))
stim2_s=visual.TextStim(winSub,text='S',color=[1,1,1],colorSpace='rgb',units='deg',height=4,pos=(-3,0))
stim3_s=visual.TextStim(winSub,text='S',color=[1,1,1],colorSpace='rgb',units='deg',height=2,pos=(0,0))

msg1x=visual.TextStim(winSub, pos=[0,+8],text='VSS localizer')
msg1a = visual.TextStim(winSub, pos=[0,+5],text='During the scan, please keep your eyes on the +',height=1)    
msg1b = visual.TextStim(winSub, pos=[0,+2],text='Hit any button any time the + becomes an X.',height=1)    
msg1=visual.TextStim(winSub,pos=[0,-3],text='Subject: Hit a key when ready.',color=[1,-1,-1],colorSpace='rgb')
msg1.draw()
msg1a.draw()
msg1b.draw()
msg1x.draw()
fix0.draw()
fix1.draw()
fix2.draw()
winSub.flip()


#wait for subject
thisKey=None
while thisKey==None:
    thisKey = event.waitKeys(keyList=['r','g','b','y','q','escape'])
if thisKey in ['q','escape']:
    core.quit() #abort
else:
    event.clearEvents()        


msg1a = visual.TextStim(winSub, pos=[0,+5],text='   ',height=1)    
msg1b = visual.TextStim(winSub, pos=[0,+2],text='Waiting for magnet',height=1)    
#msg1c.draw()
msg1a.draw()
msg1b.draw()
fix0.draw()
fix1.draw()
fix2.draw()
winSub.flip()
  
#wait for trigger
trig=None
while trig==None:
    #wait for trigger "keypress"
    trig=event.waitKeys(keyList=['t','5','q','escape'])
if trig in ['q','escape']:
    core.quit()
else: #stray key
    event.clearEvents()


#start the timer            
scanTimer=core.Clock()
startTime=scanTimer.getTime()
timeNow=scanTimer.getTime()
msg = visual.TextStim(winOp,pos=[0,0],text = 't = %.3f' %timeNow)
msg.draw()
#    trialTimer=core.Clock()
#    trialTime=trialTimer.getTime()
trialTimerNew=core.CountdownTimer()
fixTimer=core.Clock() 
respTimer=core.Clock()
#start counters for each list
Acounter=0
Bcounter=0
Ccounter=0
respCounter=0
numCoins=0
#loop through the number of trials, presenting appropriate stimulus or rest 
for iTrial in xrange(numTrials):
#        print iTrial
#        print designMatrix[iTrial,:]  
    flipCoin=numpy.random.ranf()
    if flipCoin<fixPercentage: 
        #change fixation size
        fixOri=45
        fixTimer.reset()
        respTimer.reset()
        numCoins+=1
        subjectResponse[numCoins]=0
    fixTimeCheck=fixTimer.getTime()
    respTimeCheck=respTimer.getTime()
    if fixTimeCheck>fixDuration:
        fixOri=0
    fix1.setOri(fixOri)
    fix2.setOri(fixOri)
    #dispay stim for stimDuration amount of time 
    trialTimerNew.add(stimDur)
    while trialTimerNew.getTime()>0:
        timeNow = scanTimer.getTime()
        #trialTime=trialTimer.getTime()
        #print trialTimerNew.getTime()            
        if designMatrix[iTrial,0]==1:
            stim3_s.draw()
            stim2_s.draw()
            stim1_v.draw()
        fix0.draw()
        fix1.draw()
        fix2.draw()
            
        msg.setText('t = %.3f' %timeNow)
        msg.draw()
        winSub.flip()
        winOp.flip()
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1
    trialTimerNew.add(trialLength-stimDur)
    while trialTimerNew.getTime()>0:
        #then show fixation for ISI time 
        timeNow = scanTimer.getTime()
        #add decision about fixation point changing here
        #trialTime=trialTimer.getTime()
        fix0.draw()
        fix1.draw()
        fix2.draw()
        msg.setText('t = %.3f' %timeNow)
        msg.draw()
        winSub.flip()
        winOp.flip()
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1
    #reset trial counter
    #trialTimer.reset()
    #somewhere, add in sucbject response
    #count number of keypresses since previous frame, break if non-zero
core.wait(2)
winOp.close()
winSub.close()
