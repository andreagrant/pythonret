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

#############################################################################
################### object localizer ###################################
#############################################################################
    
def objectScan(scanDict, screenSize=[1024,768], direction = 1.0):
#def motionScan(scanInfo, screen, IR = 0.5, OR = 12.0, dotSpeed=5.8, dotMotion='radial',direction = 1.0):
    scanLength = float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    #count number of screens
    if scanDict['operatorScreen']==scanDict['subjectScreen']:
        screenCount=1
    else:
        screenCount=2
    thisPlatform=scanDict['platform']
    screenSize=scanDict['screenSize']
    #if there is only one window, need to display the winOp stuff and then clear it

    if screenCount==1:
        #pop up the Tr info and wait for "ok"
        winOp = visual.Window([500,500],monitor='testMonitor',units='norm',screen=scanDict['operatorScreen'],
                                  color=[0.0,0.0,0.0],colorSpace='rgb')
        msgScanLength=visual.TextStim(winOp,pos=[0,0.5],units='norm',height=0.1,text='Scan length (s): %.1f' %scanLength)
        msgScanTr=visual.TextStim(winOp,pos=[0,0],units='norm',height=0.1,text='No. of Volumes (at Tr=%.2f): %.1f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
        msgOK=visual.TextStim(winOp,pos=[0,-0.5],units='norm',height=0.1,text='Operator, press any key to proceed')
        msgScanLength.draw()
        msgScanTr.draw()
        msgOK.draw()
        winOp.flip()
        #wait for keypress
        thisKey=None
        while thisKey==None:
            thisKey = event.waitKeys()
        if thisKey in ['q','escape']:
            core.quit() #abort
        else:
            event.clearEvents()
        #close the winOp
        winOp.close()
    else:
        winOp = visual.Window([500,500],monitor='testMonitor',units='norm',screen=scanDict['operatorScreen'],
                              color=[0.0,0.0,0.0],colorSpace='rgb')
        msgScanLength=visual.TextStim(winOp,pos=[0,0.5],units='norm',height=0.1,text='Scan length (s): %.1f' %scanLength)
        msgScanTr=visual.TextStim(winOp,pos=[0,0],units='norm',height=0.1,text='No. of Volumes (at Tr=%.2f): %.1f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
        msgScanLength.draw()
        msgScanTr.draw()
        winOp.flip()
    #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'], 
                       color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=False,allowGUI=False)
    #parse out vars from scanDict
    IR=scanDict['innerRadius']
    #OR=scanDict['outerRadius']
    #get actual size of window--useful in the functions
    subWinSize=winSub.size
    screenSize=numpy.array([subWinSize[0],subWinSize[1]])
    fixPercentage=scanDict['fixFraction']
    fixDuration=0.2
    respDuration=1.0
    subjectResponse=numpy.zeros((numpy.ceil(scanLength*60/100),1))
    subjectResponse[:]=numpy.nan
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]
    #dotAperture=OR
    quitKeys=['q','escape']

    #prepare the images so I can load them on the fly
    #pre-loading all of them causes out of memory error
    #how many images do I need
    if direction==1:
        #show scrambleds for pre=session, so first full cycle starts with intact
        getInt=(scanDict['numCycles']*scanDict['period']/2.0)/0.5
        getScr=(scanDict['numCycles']*scanDict['period']/2.0 + scanDict['preScanRest'])/0.5
    else:
        #show intacts for pre=session, so first full cycle starts with scrambled
        getInt=(scanDict['numCycles']*scanDict['period']/2.0 + scanDict['preScanRest'])/0.5
        getScr=(scanDict['numCycles']*scanDict['period']/2.0)/0.5

    #get the *list* of regular image files
    #start from the file's directory
    myPath=os.path.dirname(os.path.realpath(__file__))
    #intactImages=glob.glob(os.path.join(myPath,'intact_images512','*.TIF'))
    intactImages=glob.glob(os.path.join(myPath,'intact_images512','*.png'))
    if len(intactImages)==0:
        intactImages=glob.glob(os.path.join(myPath,'intact_images512','*.PNG'))
    if len(intactImages)==0:
        print('no intact object images found')
        core.quit()
    #sometimes they are lowercase extensions
#    if len(intactImages)==0:
#        intactImages=glob.glob(os.path.join(myPath,'intact_images512','*.tif'))
    #create a random array, then store the filenames for loading as we get to them
    numIntact=len(intactImages)
    intactImNum=numpy.arange(numIntact)
    numpy.random.shuffle(intactImNum)
    #now do this for the scrambleds    
    myPath=os.path.dirname(os.path.realpath(__file__))
    Aimages=glob.glob(os.path.join(myPath,'scrambled_images512','*.png'))
    if len(Aimages)==0:
        Aimages=glob.glob(os.path.join(myPath,'scrambled_images512','*.PNG'))
    if len(Aimages)==0:
        print('no scrambled object images found')
        core.quit()
    #print myPath
    #print Aimages
    scramImages=Aimages
#    scramImages=glob.glob(os.path.join(myPath,'scrambled_images512','*.TIF'))
    #sometimes they are lowercase extensions
#    if len(intactImages)==0:
#        scramImages=glob.glob(os.path.join(myPath,'scrambled_images512','*.tif'))
    #print myPath
    #print scramImages
    numScram=len(scramImages)
    scramImNum=numpy.arange(numScram)
    numpy.random.shuffle(scramImNum)
    
    #now make a SINGLE list of the filenames, alternating intacts and scrambleds
    #this makes the display loop much easier--just show the next image--all the work
    #of sequencing them is done here
    numInBlock=scanDict['period']#whoa--half a period but 2 images/second = the original number!
    totalImageNumber=(scanDict['preScanRest']*2+scanDict['numCycles']*scanDict['period']*2)
    imageNameSequence=['']*totalImageNumber
    imagesPerCycle=scanDict['period']*2
    if direction==1:
        #"on" condition are intact images
        #pre-scan are scrambled images
        if scanDict['preScanRest']>0:
            #need 2 images per second, but count from zero to find the number of images (preInd)
            preInd=scanDict['preScanRest']*2
            #load up that many images into the sequence buffer
            for iShuffle in range(preInd):
                imageNameSequence[iShuffle]=scramImages[scramImNum[iShuffle]]
        else:
            preInd=0
        #now, load up the rest of them
        for iIm in range(scanDict['numCycles']):
            #for each cycle, load 1/2 cycle worth of intact and 1/2cycle of scrambled
            #but offset my indices by the preInd amount
            startIndNew=preInd+iIm*imagesPerCycle
            #midInd is midPoint, which should be the starting point plus half the number per cycle
            midIndNew=startIndNew+numInBlock
            #now I have the indices of the destination list
            for iFullSequence in range(numInBlock):
                #also need images for the source list, which increments half as much
                sourceInd=preInd+iIm*numInBlock+iFullSequence
                imageNameSequence[startIndNew+iFullSequence]=intactImages[intactImNum[sourceInd]]
                imageNameSequence[midIndNew+iFullSequence]=scramImages[scramImNum[sourceInd]]
    else:
        #pre-scan is intact, "on" condition are scrambled images
        if scanDict['preScanRest']>0:
            preInd=scanDict['preScanRest']*2
            for iShuffle in range(preInd):
                imageNameSequence[iShuffle]=intactImages[intactImNum[iShuffle]]
        else:
            preInd=0
        for iIm in range(scanDict['numCycles']):
            startIndNew=preInd+iIm*imagesPerCycle
            midIndNew=startIndNew+numInBlock
            for iFullSequence in range(numInBlock):
                sourceInd=preInd+iIm*numInBlock+iFullSequence
                imageNameSequence[startIndNew+iFullSequence]=scramImages[scramImNum[sourceInd]]
                imageNameSequence[midIndNew+iFullSequence]=intactImages[intactImNum[sourceInd]]
    #print imageNameSequence
    #create a dictionary of the images but load only the first one
    #load the first image
    currentImageNumber=0
    #print imageNameSequence
    imageStimDict=dict.fromkeys(numpy.arange(0,numIntact+numScram))
    imageStimDict[currentImageNumber]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber])
#    nextImage=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber+1])
    nextImLoadedFlag=0
    
#    #debug 
#    for iD in range(504):
#        print(iD)
#        print(imageNameSequence[iD])

    #fixation
    fix0=visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
                       fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',
                            fillColor=black,fillColorSpace='rgb',autoLog=False)
    fix2 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((-0.15,0),(0.15,0.0)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',autoLog=False)
    
    #wait for subject    
    if direction==1:
        scanNameText='Object localizer. On condition is %s images' % ('intact')
    else:
        scanNameText='Object localizer. On condition is %s images' % ('scrambled')
        
    msg1=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msg1.draw()
    winSub.flip()
    thisKey=None
    responseKeys=list(scanDict['subjectResponse'])
    responseKeys.extend('q')
    responseKeys.extend('escape')
    while thisKey==None:
        thisKey=event.waitKeys(keyList=responseKeys)
    if thisKey in quitKeys:
        core.quit()
    else:
        event.clearEvents()
    responseKeys=list(scanDict['subjectResponse'])

    #wait for trigger
    msg1.setText('Noise Coming....')
    msg1.draw()
    winSub.flip()
    trig=None
    triggerKeys=list(scanDict['trigger'])
    triggerKeys.extend('q')
    triggerKeys.extend('escape')
    while trig==None:
        trig=event.waitKeys(keyList=triggerKeys)
    if trig in quitKeys:
        core.quit()
    else:
        event.clearEvents()
    
    #start the timer
    scanTimer=core.Clock()
    startTime=scanTimer.getTime()
    #draw the fixation
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()
    
    #draw the time
    timeNow=scanTimer.getTime()
#    timeMsg=visual.TextStim(winSub,pos=[-screenSize[0]/2+100,-screenSize[1]/2+15],units='pix',text= 't = %.3f' %timeNow)
    if screenCount==2:     
        timeMsg = visual.TextStim(winOp,pos=[0,-0.5],text = 't = %.3f' %timeNow)
        timeMsg.draw()
    loopCounter=0
    fixTimer=core.Clock()
    respTimer=core.Clock()
    flipTimer=core.Clock()
    fixOri=0
    numCoins=0
    phaseSign=1.0
    epochTimer = core.Clock()
    miniEpochTimer=core.Clock()
    event.clearEvents()

    #draw images--the sequence of intact/scrambled was set previously
    while timeNow<startTime+scanLength:
        timeBefore=timeNow#um, is this aliasing?
        timeNow=scanTimer.getTime()
        deltaT=timeNow-timeBefore
        runningT=timeNow-startTime
        
        #every 100 frames, decide if fixation should change or not    
        if loopCounter%100 ==0 and loopCounter>10:
           #flip a coin to decide
            flipCoin=numpy.random.ranf()
            if flipCoin<fixPercentage: 
                #reset timers/change ori
                fixOri=45
                fixTimer.reset()
                respTimer.reset()
                numCoins+=1
                subjectResponse[numCoins]=0
        fixTimeCheck=fixTimer.getTime()
        respTimeCheck=respTimer.getTime()
        if fixTimeCheck >fixDuration: #timer expired--reset ori
            fixOri=0
        miniEpochTime=miniEpochTimer.getTime()
        #check to see if the next image is loaded
        if nextImLoadedFlag==0:
            #load it
            #if we haven't already reached the end
            if currentImageNumber<totalImageNumber-1:
                imageStimDict[currentImageNumber+1]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber+1])
            #delete the previous one (well, the 2nd previous one)
            if currentImageNumber>3:
                del imageStimDict[currentImageNumber-1]
            #reset the flag            
            nextImLoadedFlag=1

        #every 0.5 seconds, change the image  
        if miniEpochTime>0.5:
            #bump the image counter
            currentImageNumber+=1
            #reset the loading flag
            nextImLoadedFlag=0
            if currentImageNumber==(scanDict['preScanRest']+scanDict['numCycles']*scanDict['period'])*2:
                #already have last image
                nextImLoadedFlag=1
            #reset the timer
            miniEpochTimer.reset()
        #draw my image, whatever it is
        imageStimDict[currentImageNumber].draw()
        #debugging--print previous, current, and next image
#        if currentImageNumber>1:
#            print(currentImageNumber)
#            print(imageStimDict[currentImageNumber-1])
#            print(imageStimDict[currentImageNumber])
#            print(imageStimDict[currentImageNumber+1])
#        
        fix1.setOri(fixOri)
        fix2.setOri(fixOri)   
        fix0.draw()
        fix1.draw()
        fix2.draw()
        winSub.flip()
        if screenCount==2:
            timeMsg.setText('t = %.3f' %timeNow)
            timeMsg.draw()
            msgScanLength.draw()
            msgScanTr.draw()
            winOp.flip()


        #look for responses
        for key in event.getKeys():
            if key in quitKeys:
                core.quit()
            elif key in responseKeys and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1
        
        loopCounter+=1
         
    #check responses
    findResp=subjectResponse[~numpy.isnan(subjectResponse)]
    calcResp=findResp[findResp==1]
    numCorrect=float(calcResp.shape[0])
    if numCoins>0:
        percentCorrect=100.0*float(numCorrect)/(float(numCoins))
    else:
        percentCorrect=100.0
    
    msgText='You got %.0f %% correct!' %(percentCorrect,)
    msgPC=visual.TextStim(winSub,pos=[0,+3],text=msgText)
    msgPC.draw()
    winSub.flip()

#    numpy.savetxt('debug.txt',debugVar,fmt='%.3f')
    #create an output file in a subdirectory
    #check for the subdirectory
    if os.path.isdir('subjectResponseFiles')==False:
        #create directory
        os.makedirs('subjectResponseFiles')
    nowTime=datetime.datetime.now()
    outFile='objectResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    if screenCount==2:
        winOp.close()
    winSub.close()
