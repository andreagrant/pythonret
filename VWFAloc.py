#import libraries
from __future__ import division
from psychopy import visual
from psychopy import gui
from psychopy import core
from psychopy import data
from psychopy import misc
from psychopy import event
from psychopy import filters
from psychopy import monitors
import time, numpy, random
#import retinotopyScans
import math
from array import *
import os
import glob
import imp
import datetime

##########################################################################
##########################################################################
################################### VWFA localizer ############################
##########################################################################
##########################################################################

def VWFAloc(scanDict,screenSize=[1024,768]):

    #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'], 
                       color=[-1.0,-1.0,-1.0],colorSpace='rgb',fullscr=True,allowGUI=False)
    winOp = visual.Window([500,200],monitor='testMonitor',units='deg',screen=scanDict['operatorScreen'],
                          color=[0.0,0.0,0.0],colorSpace='rgb')
    fixPercentage =scanDict['fixFraction']
    fixDuration=0.25
    respDuration=1.0
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]
    IR=scanDict['innerRadius']
    screenSize=scanDict['screenSize']

    #create a designmatrix 
    numTrials=228
    designMatrix=numpy.zeros((numTrials,3))  
    numEach=36#36 of each type

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
    designMatrix[12:23,0]=1
    designMatrix[108:119,0]=1
    designMatrix[204:215,0]=1
    designMatrix[36:47,1]=1
    designMatrix[84:95,1]=1
    designMatrix[156:167,1]=1
    designMatrix[60:71,2]=1
    designMatrix[132:143,2]=1
    designMatrix[180:191,2]=1

    #length of scan in s
    scanLength=numTrials*trialLength
    msgScanLength=visual.TextStim(winOp,pos=[0,2],text='Scan length (s): %.1f' %scanLength)
    msgScanTr=visual.TextStim(winOp,pos=[0,1],text='No. of Volumes (at Tr=%.2f): %.0f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
    msgScanLength.draw()
    msgScanTr.draw()
    winOp.flip()

    subjectResponse=numpy.zeros((numpy.ceil(scanLength*60/100),1))
    subRespArray=numpy.zeros((numpy.ceil(scanLength*60/100),3))
    subjectResponse[:]=numpy.nan

    #prep display objects
    #letters, nonletters, emoticons
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
#    Clist=[u"\u1F600",u"\u1F601",u"\u1F602",u"\u1F603",u"\u1F604",u"\u1F605",u"\u1F606",u"\u1F607",u"\u1F608",
#               u"\u1F609",u"\u1F60A",u"\u1F60B",u"\u1F60C",u"\u1F60D",u"\u1F60E",u"\u1F60F",u"\u1F610",u"\u1F611",
#               u"\u1F612",u"\u1F613",u"\u1F614",u"\u1F615",u"\u1F616",u"\u1F617",u"\u1F618",u"\u1F619",u"\u1F61A",
#               u"\u1F61B",u"\u1F61C",u"\u1F61D",u"\u1F61E",u"\u1F61F",u"\u1F620",u"\u1F621",u"\u1F622",u"\u1F623",
#               u"\u1F624",u"\u1F625",u"\u1F626",u"\u1F627",u"\u1F628",u"\u1F629",u"\u1F62A",u"\u1F62B",u"\u1F62C",
#               u"\u1F62D",u"\u1F62E",u"\u1F62F",u"\u1F630",u"\u1F631",u"\u1F632",u"\u1F633",u"\u1F634",u"\u1F635",
#               u"\u1F636",u"\u1F637",u"\u1F638",u"\u1F639",u"\u1F63A",u"\u1F63B",u"\u1F63C",u"\u1F63D",u"\u1F63E",u"\u1F63F"]
    Clist=["1F600","1F601","1F602","1F603","1F604","1F605","1F606","1F607","1F608",
               "1F609","1F60A","1F60B","1F60C","1F60D","1F60E","1F60F","1F610","1F611",
               "1F612","1F613","1F614","1F615","1F616","1F617","1F618","1F619","1F61A",
               "1F61B","1F61C","1F61D","1F61E","1F61F","1F620","1F621","1F622","1F623",
               "1F624","1F625","1F626","1F627","1F628","1F629","1F62A","1F62B","1F62C",
               "1F62D","1F62E","1F62F","1F630","1F631","1F632","1F633","1F634","1F635",
               "1F636","1F637","1F638","1F639","1F63A","1F63B","1F63C","1F63D","1F63E","1F63F"]
    myPath=os.path.dirname(os.path.realpath(__file__))           
    Cimages=glob.glob(os.path.join(myPath,'unicodeEmoticons','*.png'))
    numInList=numpy.zeros((3,1))
    numInList[0]=len(Alist)
    numInList[1]=len(Blist)
    numInList[2]=len(Cimages)
    #generate my random sequence --need 36 of each list
    Asequence=numpy.random.randint(0,high=numInList[0],size=36)
    Bsequence=numpy.random.randint(0,high=numInList[1],size=36)
    Csequence=numpy.random.randint(0,high=numInList[2],size=36)
    
    imageNameSequence=['']*numEach
    for iIm in xrange(numEach):
        imageNameSequence[iIm]=Cimages[Csequence[iIm]]
    imageStimDict=dict.fromkeys(numpy.arange(0,numEach))
    currentImageNumber=0
    imageStimDict[currentImageNumber]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber])
    numpy.savetxt('designMatrix.txt',designMatrix,fmt='%.3i')


    #make a fixation cross which will rotate 45 deg on occasion
    #this will be a problem. Need a square that embiggens
    fixSize=IR/2.0
    fix0 = visual.Rect(winSub,width=fixSize,height=fixSize,autoLog=False)
    fix0.setFillColor(color=gray,colorSpace='rgb')
    fix0.setLineColor(color=[1,-1,-1],colorSpace='rgb')
#    fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.2),(0.0,0.2)),lineWidth=3.0,
#            lineColor=black,lineColorSpace='rgb',
#            fillColor=black,fillColorSpace='rgb',autoLog=False)
#    
#    fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.2,0.0),(0.2,0.0)),lineWidth=3.0,
#            lineColor=black,lineColorSpace='rgb',
#            fillColor=black,fillColorSpace='rgb',autoLog=False)
 
 
 
    #create the unicode text stimulus
#    thisText="u"+"\""+Alist[0]+"\""
#    thisText="\""+Alist[0]+"\""
    
    #actualStim=visual.TextStim(winSub,text=Alist[0],color=black,colorSpace='rgb',units='degrees',height=1,pos=(0,0))
    actualStim=visual.TextStim(winSub,text=Alist[1],color=gray,colorSpace='rgb',units='deg',height=2,pos=(0,0))
    
    msg1x=visual.TextStim(winSub, pos=[0,+8],text='visual wordform area localizer')
    msg1a = visual.TextStim(winSub, pos=[0,+5],text='During the scan, please keep your eyes on the + in the center.',height=1)    
    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Hit any button any time the + becomes an X.',height=1)    
    msg1=visual.TextStim(winSub,pos=[0,-3],text='Subject: Hit a button when ready.',color=[1,-1,-1],colorSpace='rgb')
    msg1.draw()
    msg1a.draw()
    msg1b.draw()
    msg1x.draw()
    fix0.draw()
#    fix1.draw()
#    fix2.draw()
    winSub.flip()


    #wait for subject
    thisKey=None
    while thisKey==None:
        thisKey = event.waitKeys(keyList=['r','g','b','y','1','2','3','4','q','escape'])
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
    #fix1.draw()
    #fix2.draw()
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
    msg = visual.TextStim(winOp,pos=[0,-1],text = 't = %.3f' %timeNow)
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
        respTimer.reset()        
        flipCoin=numpy.random.ranf()
        if flipCoin<fixPercentage: 
            #change fixation size
            fixSize*=1.25
            fixTimer.reset()
            respTimer.reset()
            numCoins+=1
            subjectResponse[numCoins]=0
        fix0.setWidth(fixSize)
        fix0.setHeight(fixSize)
        if designMatrix[iTrial,0]==1:
            #Alist
            #get stim
            thisA=Asequence[Acounter]
            thisText=Alist[thisA]
            Acounter+=1
            drawFix=0
            actualStim.setText(thisText)
            stimType=0
        elif designMatrix[iTrial,1]==1:
            #Blist
            #get stim
            thisB=Bsequence[Bcounter]
            thisText=Blist[thisB]
            drawFix=0
            Bcounter+=1
            actualStim.setText(thisText)
            stimType=0
        elif designMatrix[iTrial,2]==1:
            #Clist
            #get stim
#            thisC=Csequence[Ccounter]
#            thisText=Clist[thisC]
            currentImageNumber+=1            
            if currentImageNumber+1<len(imageNameSequence): #don't load an image past the last one!
                imageStimDict[currentImageNumber+1]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber+1])
            if currentImageNumber>3:
                del imageStimDict[currentImageNumber-1]
            Ccounter+=1
            drawFix=0
            stimType=1
        else:
            #rest 
            thisText=""
            drawFix=1
            fix0.draw()
            stimType=0
            actualStim.setText(thisText)
            #fix1.draw()
            #fix2.draw()
        
        #dispay stim for stimDuration amount of time 
        trialTimerNew.add(stimDur)
        while trialTimerNew.getTime()>0:
            timeNow = scanTimer.getTime()
            #trialTime=trialTimer.getTime()
            #print trialTimerNew.getTime()            
            fixTimeCheck=fixTimer.getTime()
            respTimeCheck=respTimer.getTime()
            if fixTimeCheck>fixDuration:
                fixSize=IR/2.0
            if stimType==0:
                actualStim.draw()
            else:
                imageStimDict[currentImageNumber].draw()
            if drawFix==1:
                fix0.draw()
                #fix1.draw()
                #fix2.draw()
                
            msg.setText('t = %.3f' %timeNow)
            msg.draw()
            winSub.flip()
            winOp.flip()
            for key in event.getKeys():
                if key in ['q','escape']:
                    core.quit()
                elif key in ['r','g','b','y','1','2','3','4'] and respTimeCheck<respDuration:
                    subjectResponse[numCoins]=1
        trialTimerNew.add(trialLength-stimDur)
        while trialTimerNew.getTime()>0:
            #then show fixation for ISI time 
            timeNow = scanTimer.getTime()
            fixTimeCheck=fixTimer.getTime()
            respTimeCheck=respTimer.getTime()
            if fixTimeCheck>fixDuration:
                fixSize=IR/2.0
          #add decision about fixation point changing here
            #trialTime=trialTimer.getTime()
            fix0.draw()
            #fix1.draw()
            #fix2.draw()
            msg.setText('t = %.3f' %timeNow)
            msg.draw()
            winSub.flip()
            winOp.flip()
            for key in event.getKeys():
                if key in ['q','escape']:
                    core.quit()
                elif key in ['r','g','b','y','1','2','3','4'] and respTimeCheck<respDuration:
                    subjectResponse[numCoins]=1
        #reset trial counter
        #trialTimer.reset()
        #somewhere, add in sucbject response
        #count number of keypresses since previous frame, break if non-zero
    findResp=subjectResponse[~numpy.isnan(subjectResponse)]
    calcResp=findResp[findResp==1]
    numCorrect=float(calcResp.shape[0])
    if numCoins>0:
        percentCorrect=100.0*float(numCorrect)/(float(numCoins))
    else:
        percentCorrect=100.0
    
    msgText='You got %.0f %% correct!' %(percentCorrect,)
    msg1=visual.TextStim(winSub,pos=[0,+3],text=msgText)
    msg1.draw()
    winSub.flip()

    #create an output file in a subdirectory
    #check for the subdirectory
    if os.path.isdir('subjectResponseFiles')==False:
        #create directory
        os.makedirs('subjectResponseFiles')
    nowTime=datetime.datetime.now()
    outFile='vwfaResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    winSub.close()
    winOp.close()

  