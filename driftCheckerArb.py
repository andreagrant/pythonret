# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:44:34 2015

@author: agrant
"""

#import libraries
from psychopy import visual
from psychopy import gui
from psychopy import core
from psychopy import data
from psychopy import misc
from psychopy import event
from psychopy.visual import filters
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
################### drifting checkerboard ###################################
#############################################################################
def driftCheckerArb(scanDict,screenSize=[1024,768],offTimeBehavior=1,maskType=1):

    #offtimeBehaior:
        #1--full field, drift vs rest
        #2--full field, drift vs static
        #3--full field masked
        #           mask = 1: center vs surround
        #           mask = 2: alternating halves (left vs right)

    #20151222 adding two options:
    # 1) arbitrary timing for cond A vs cond B vs rest
    # 2) inclusion of possible rest (gray screen)...
    #issues: how flexible can the timing be? blocks of A/B with rest in between?

# "period" timing: duration of A and B (no longer Period/2)
# "block details": number of reps per block (AB or ABAB or ABABAB ....) abd number of blocks
# "rest details"---duration of rest after each block (see above)    and rest at beginning/end (which is lready there)

    durA=scanDict['stimDurationA']
    durB=scanDict['stimDurationB']
    durRest=scanDict['stimDurationRest']

    #length of scan in s
    blockLength=(scanDict['numReps']*(durA+durB))+durRest
    scanLength=float(scanDict['numBlocks']*blockLength+scanDict['preScanRest']+scanDict['postScanRest'])

    #This structure is much more complicated and I need to create a sort of design matrix
    #2 stim types (A&B)* numReps + 1 rest in a block ... times the numebr of blocks .... +rest on eitehr end
    numEvents=(2*scanDict['numReps']+1)*scanDict['numBlocks']+2
    #create a designmatrix with the event type (rest, A, B) and OFFset time
    designMatrix=numpy.zeros((numEvents,2))
    #prescan rest
    designMatrix[0][0]=0#event type
    designMatrix[0][1]=scanDict['preScanRest']#end time

    #loop through blocks and then reps
    iEvent=1
    for iBlock in range(scanDict['numBlocks']):
        for iRep in range(scanDict['numReps']):
            #stim A
            designMatrix[iEvent][0]=1 #event type
            designMatrix[iEvent][1]=designMatrix[iEvent-1][1]+durA  #END time
            iEvent+=1
            #stim b
            designMatrix[iEvent][0]=2 #event type
            designMatrix[iEvent][1]=designMatrix[iEvent-1][1]+durB  #END time
            iEvent+=1
        #rest after nReps
        designMatrix[iEvent][0]=0 #event type
        designMatrix[iEvent][1]=designMatrix[iEvent-1][1]+durRest  #END time
        iEvent+=1

    #post-scanrest
    designMatrix[iEvent][0]=0 #event type
    designMatrix[iEvent][1]=designMatrix[iEvent-1][1]+scanDict['postScanRest']  #END time
    numpy.savetxt('debug.txt',designMatrix)
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
    print(screenSize)
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units='deg',screen=scanDict['subjectScreen'],
                           color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=False,allowGUI=False)

    #parse out vars from scanDict
    IR=scanDict['innerRadius']
    OR=scanDict['outerRadius']
    contrast=scanDict['contrast']
    #get actual size of window--useful in the functions
    subWinSize=winSub.size
    screenSize=numpy.array([subWinSize[0],subWinSize[1]])
    fixPercentage = scanDict['fixFraction']
    fixDuration=0.2
    respDuration=1.0
    dummyLength=int(numpy.ceil(scanLength*60/100))
    subjectResponse=numpy.zeros(( dummyLength,1))
    subjectResponse[:]=numpy.nan
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]

    #print winSub.fps()

    #test "refresh" rate
    #[frameTimeAvg,frameTimeStd,frameTimeMed] = visual.getMsPerFrame(winSub,nFrames=120, showVisual=True, msg='', msDelay=0.0)
    #print frameTimeAvg
    #print frameTimeMed
    #refreshRate = 1000.0/frameTimeMed
    #runInfo=psychopy.info.RunTimeInfo(win = winSub,refreshTest='grating',verbose=True)
    #print runInfo
    #create stimulus
    #make 3 wedges, each 7.5 degrees wide, with opposite phase
    #use visibleWedge=[0, 45]???
    #initial orientations
    wedgeSize=[0.0,18]
    startOris = range(0,360,18)
    startPhases=numpy.random.rand(10)
#    wedgeWidth=360.0/12.0
    numRadialCycles = OR/2.0
 #   wedgeOriInit=numpy.arange(0,360,30)
 #   wedgeSize=[0.0,30.0]
    wedge1 = visual.RadialStim(winSub,pos = [0, 0],tex='sqrXsqr',radialCycles=numRadialCycles,
         angularCycles=0,
         size=OR*2,color=1,visibleWedge=wedgeSize,ori=0,interpolate=False,contrast=contrast,
         autoLog=False)

    altWedges=numpy.random.rand(10)
    for iGrr in range(0,10):
        altWedges[iGrr]=(-1)**iGrr
    #organize the masks for the two masked runs
    if offTimeBehavior==3 and maskType==1:
        #center surround
        #mask out just the parts necessary
        #make a square array filled with radii
        myfilter=filters.makeRadialMatrix(512)
        #mask surround to show only the center
        myAnn=numpy.where(myfilter*OR>4.0,1,0)*2-1
        maskA=visual.GratingStim(winSub,tex=None,mask=myAnn,units='pix',size=screenSize[0],color=gray,colorSpace='rgb')
        #mask the center to show the surround
        myAnn2=numpy.where(myfilter*OR<4.0,1,0)*numpy.where(myfilter*OR>0,1,0)*2-1
        maskB=visual.GratingStim(winSub,tex=None,mask=myAnn2,units='pix',size=screenSize[0],color=gray,colorSpace='rgb')
    elif offTimeBehavior==3 and maskType==2:
        #left and right masks
        maskA=visual.Rect(win=winSub,units='norm',pos=(-0.5,0),width=1.0, height=2.0,fillColor=gray,fillColorSpace='rgb',lineColor=None)
        maskB=visual.Rect(win=winSub,units='norm',pos=(0.5,0),width=1.0, height=2.0,fillColor=gray,fillColorSpace='rgb',lineColor=None)

    driftFreq=scanDict['animFreq']
    driftReverseFreq = 0.5 #Hz

    #make a fixation cross which will rotate 45 deg on occasion
    fix0 = visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
            fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)

    fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.15,0.0),(0.15,0.0)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)


    if offTimeBehavior==1:
        scanNameText='drifting checkerboard, on/off'
    elif offTimeBehavior==2:
        scanNameText='drifting checkerboard, drift/static'
    else:
        if maskType==1:
            scanNameText='drifting checkerboard, center/surround'
        else:
            scanNameText='drifting checkerboard, alternating halves'

    msgSB=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msgSB.draw()
    winSub.flip()

    #wait for subject
    thisKey=None
    responseKeys=list(scanDict['subjectResponse'])
    responseKeys.extend('q')
    responseKeys.extend('escape')
    while thisKey==None:
        thisKey = event.waitKeys(keyList=responseKeys)
    if thisKey in ['q','escape']:
        core.quit() #abort
    else:
        event.clearEvents()
#    while len(event.getKeys())==0:
#        core.wait(0.05)
#    event.clearEvents()
    responseKeys=list(scanDict['subjectResponse'])
    msgNC=visual.TextStim(winSub,pos=[0,+3],text='Noise coming....')
    msgNC.draw()
    winSub.flip()
    #wait for trigger
    trig=None
    triggerKeys=list(scanDict['trigger'])
    triggerKeys.extend('q')
    triggerKeys.extend('escape')
    while trig==None:
        #wait for trigger "keypress"
        trig=event.waitKeys(keyList=triggerKeys)
    if trig in ['q','escape']:
        core.quit()
    else: #stray key
        event.clearEvents()

    #start the timer
    scanTimer=core.Clock()
    startTime=scanTimer.getTime()
    epochTimer = core.Clock()
    #draw the stimulus
    for iWedge in range(0,20,2):
        wedge1.setOri(startOris[iWedge])
        wedge1.setRadialPhase(startPhases[int(iWedge/2)])
        #wedge1.draw()
        wedge1.setOri(startOris[iWedge+1])
        wedge1.setRadialPhase(startPhases[int(iWedge/2)]+0.5)
        #wedge1.draw()
    if offTimeBehavior==3:
        nowMask=maskA
        #maskA.draw()
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()
    nowPhase=startPhases
    # and drift it
    timeNow = scanTimer.getTime()
    #row=1
#    #msg = visual.TextStim(winSub, pos=[-screenSize[0]/2+45,-screenSize[1]/2+15],units='pix',text = 't = %.3f' %timeNow)
    if screenCount==2:
        msg = visual.TextStim(winOp,pos=[0,-0.5],text = 't = %.3f' %timeNow)
        msg.draw()
    loopCounter=0
    fixTimer=core.Clock()
    respTimer=core.Clock()
    fixOri=0
    numCoins=0
    event.clearEvents()

    #start the actual stimulus part

    #loop through the blocks ... which are events
    for iEvent in range(numEvents):
        #print(iEvent)
        eventType=designMatrix[iEvent][0]
        eventEnd=designMatrix[iEvent][1]
        epochTimer.reset()
        epochTime=epochTimer.getTime()
        timeNow = scanTimer.getTime()
        while timeNow<eventEnd:
            epochTime=epochTimer.getTime()
            if screenCount==2:
                msg.setText('t = %.3f' %timeNow)
                msg.draw()
                msgScanLength.draw()
                msgScanTr.draw()
                winOp.flip()
            timeBefore = timeNow
            timeNow = scanTimer.getTime()
            deltaT=timeNow - startTime
            deltaTinc=timeNow-timeBefore
            oldPhases=nowPhase.copy()
            #every 100 frames, decide if the fixation point should change or not
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
            fix1.setOri(fixOri)
            fix2.setOri(fixOri)


            #decide which stimulus should be shown

            if eventType==1:
                #stimA
                if offTimeBehavior==3:
                    nowMask=maskA
                #lastPhase=nowPhase.copy()
    #            deltaPhase=driftFreq*deltaT
                deltaPhaseInc=driftFreq*deltaTinc
                #NowPhase=lastpHase+deltaPhase
                #set direction of drift--alternate every Ns, where N is set by driftReverseFreq
                setSign=math.floor(driftReverseFreq*deltaT)
                if setSign%2==0:
                    phaseSign = 1.0
                else:
                    phaseSign = -1.0
                phaseSignVec=phaseSign*altWedges
    #            nowPhase=startPhases + deltaPhase*(phaseSignVec)
                nowPhase=oldPhases+deltaPhaseInc*(phaseSignVec)
                for iWedge in range(0,20,2):
                    wedge1.setOri(startOris[iWedge])
                    wedge1.setRadialPhase(nowPhase[int(iWedge/2)])
                    wedge1.draw()
                    wedge1.setOri(startOris[iWedge+1])
                    wedge1.setRadialPhase(nowPhase[int(iWedge/2)]+0.5*phaseSignVec[int(iWedge/2)])
                    wedge1.draw()

                if offTimeBehavior==3:
                    nowMask.draw()
                fix0.draw()
                fix1.draw()
                fix2.draw()
            elif eventType==2:
                #print('B')
                #second epoch ... stimB
                #draw either no checkerboard or static checkerboard, depending on scan
                if offTimeBehavior==1:
                    #turn it OFF
                    #just draw fixation
                    fix0.draw()
                    fix1.draw()
                    fix2.draw()
                elif offTimeBehavior==2:
                    #draw static
                    for iWedge in range(0,20,2):
                        wedge1.setOri(startOris[iWedge])
                        wedge1.setRadialPhase(nowPhase[int(iWedge/2)])
                        wedge1.draw()
                        wedge1.setOri(startOris[iWedge+1])
                        wedge1.setRadialPhase(nowPhase[int(iWedge/2)]+0.5*phaseSignVec[int(iWedge/2)])
                        wedge1.draw()

                    fix0.draw()
                    fix1.draw()
                    fix2.draw()
                elif offTimeBehavior==3:
                    #keep drifting, change mask
                    nowMask=maskB
                    #lastPhase=nowPhase.copy()
    #                deltaPhase=driftFreq*deltaT
                    deltaPhaseInc=driftFreq*deltaTinc
                    #set direction of drift--alternate every cycle
                    setSign=math.floor(driftReverseFreq*deltaT)
                    if setSign%2==0:
                        phaseSign = 1.0
                    else:
                        phaseSign = -1.0
                    phaseSignVec=phaseSign*altWedges
    #                nowPhase=startPhases + deltaPhase*(phaseSignVec)
                    nowPhase=oldPhases + deltaPhaseInc*(phaseSignVec)
                    for iWedge in range(0,20,2):
                        wedge1.setOri(startOris[iWedge])
                        wedge1.setRadialPhase(nowPhase[int(iWedge/2)])
                        wedge1.draw()
                        wedge1.setOri(startOris[iWedge+1])
                        wedge1.setRadialPhase(nowPhase[int(iWedge/2)]+0.5*phaseSignVec[int(iWedge/2)])
                        wedge1.draw()
                    nowMask.draw()
                    fix0.draw()
                    fix1.draw()
                    fix2.draw()
            elif eventType==0:
                #rest
                fix0.draw()
                fix1.draw()
                fix2.draw()

            winSub.flip()
            #row+=1
            #core.wait(3.0/60.0)

            #count number of keypresses since previous frame, break if non-zero
            for key in event.getKeys():
                if key in ['q','escape']:
                    core.quit()
                elif key in responseKeys and respTimeCheck<respDuration:
                    subjectResponse[numCoins]=1

            loopCounter +=1

        #print('end of while loop in this event')
    #calculate %age of responses that were correct
    #find non-nan
    #np.isnan(a) gives boolean array of true/a=false
    #np.isnan(a).any(1) gives a col vector of the rows with nans
    #~np.isnan(a).any(1) inverts the logic
    #myarray[~np.isnan(a).any(1)] gives the subset that I want
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

    #create an output file in a subdirectory
    #check for the subdirectory
    if os.path.isdir('subjectResponseFiles')==False:
        #create directory
        os.makedirs('subjectResponseFiles')
    nowTime=datetime.datetime.now()
    outFile='driftResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    winSub.close()
    if screenCount==2:
        winOp.close()
