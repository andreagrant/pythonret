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
import ast
#############################################################################
################### flickering checkerboard ###################################
################### asymmetric timing #######################################
#############################################################################

def flasher(scanDict, screenSize=[1024,768]):
    #do full field flickering checkerboard
    #length of scan in s
    scanLength=float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    screenSize=scanDict['screenSize']



    IR=scanDict['innerRadius']
    OR=scanDict['outerRadius']
    colorA=numpy.zeros((3,1))
    colorB=numpy.zeros((3,1))
    colorBG=numpy.zeros((3,1))
    foo=scanDict['colorA']
    if type(foo) is str:
        bar=foo.split(",")
        colorA[0]=float(bar[0])
        colorA[1]=float(bar[1])
        colorA[2]=float(bar[2])
        foo=scanDict['colorB']
        bar=foo.split(",")
        colorB[0]=float(bar[0])
        colorB[1]=float(bar[1])
        colorB[2]=float(bar[2])
        foo=scanDict['colorBackground']
        bar=foo.split(",")
        colorBG[0]=float(bar[0])
        colorBG[1]=float(bar[1])
        colorBG[2]=float(bar[2])
        #convert colors to psychopy's scheme
        colorAf=numpy.asarray(colorA,dtype=float)
        colorBf=numpy.asarray(colorB,dtype=float)
        colorBGf=numpy.asarray(colorBG,dtype=float)

    elif type(foo) is unicode:
        #this is from the params file
        #or not. the menu is suddenly making this.
        foo2=ast.literal_eval(foo)
        colorAf=numpy.asarray(foo2,dtype=float)
        foo=scanDict['colorB']
        foo2=ast.literal_eval(foo)
        colorBf=numpy.asarray(foo2,dtype=float)
        foo=scanDict['colorBackground']
        foo2=ast.literal_eval(foo)
        colorBGf=numpy.asarray(foo2,dtype=float)
    else:
        colorA=scanDict['colorA']
        colorB=scanDict['colorB']
        colorBG=scanDict['colorBackground']
        #convert colors to psychopy's scheme
        colorAf=numpy.asarray(colorA,dtype=float)
        colorBf=numpy.asarray(colorB,dtype=float)
        colorBGf=numpy.asarray(colorBG,dtype=float)

    colorAp=2*colorAf-1
    colorBp=2*colorBf-1
    colorBGp=2*colorBGf-1
    flickFreq=scanDict['animFreq']
    timeBase=0#scanDict['timeBase']
    #deal with optional color change in fixation
    try:
        if scanDict['fixationStyle']==2:
            fixColorChange=1
        else:
            fixColorChange=0
    except:
        fixColorChange=1
    fixPercentage =scanDict['fixFraction']
    fixDuration=0.25
    respDuration=1.0
    dummyLength=int(numpy.ceil(scanLength*60/100))
    subjectResponse=numpy.zeros(( dummyLength,1))
    subRespArray=numpy.zeros(( dummyLength,3))
    subjectResponse[:]=numpy.nan

    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]

    if scanDict['operatorScreen']==scanDict['subjectScreen']:
        screenCount=1
    else:
        screenCount=2
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
        winOp = visual.Window([700,500],monitor='testMonitor',units='norm',screen=scanDict['operatorScreen'],
                              color=[0.0,0.0,0.0],colorSpace='rgb')
        msgScanLength=visual.TextStim(winOp,pos=[0,0.5],units='norm',height=0.1,text='Scan length (s): %.1f' %scanLength)
        msgScanTr=visual.TextStim(winOp,pos=[0,0],units='norm',height=0.1,text='No. of Volumes (at Tr=%.2f): %.1f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
        msgScanLength.draw()
        msgScanTr.draw()
        winOp.flip()
        #create subject response messages
        msgRespRecent=visual.TextStim(winOp,pos=[0,0],units='pix',text='',height=40)
        msgResponse=visual.TextStim(winOp,pos=[0,-200],units='pix',text='',height=40)


   #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'],
                       color=colorBGp,colorSpace='rgb',fullscr=True,allowGUI=False)

    #create a background-colored rectangle to try and fix the problem of opwin messages showin up on subwin
    blank=visual.Rect(winSub,fillColor=colorBGp,fillColorSpace='rgb',lineColor=colorBGp,lineColorSpace='rgb',width=screenSize[0],height=screenSize[1],units='pix')
    #create a designmatrix for trigger-based counting
    #first create an array--length = total number of Trs
    numTr=scanLength/scanDict['Tr']
    designMatrix=numpy.zeros((numTr,1))

    #first N Trs are already zero--rest
    #figure out when the stim should be on
    for iStim in range(scanDict['numCycles']):
        restAmt=scanDict['preScanRest']/scanDict['Tr']
        stimDur=scanDict['period']/scanDict['Tr']
        firstVal=restAmt + iStim*stimDur
        lastVal=firstVal + scanDict['period']/(2*scanDict['Tr'])
        designMatrix[firstVal:lastVal]=1
    numpy.savetxt('debug.txt',designMatrix,fmt='%.3i')


    debugVar=numpy.zeros((scanLength*60,2))
    if screenSize[0]<257:
        imageSize=256
    elif screenSize[0]<513:
        imageSize=512
    elif screenSize[0]<1025:
        imageSize=1024
    elif screenSize[0]<2057:
        imageSize=2048
    halfSize=numpy.int(imageSize/2)

    #create arrays of x,y, and r,theta
    xIn=numpy.arange(-halfSize,halfSize,1)
    yIn=numpy.arange(-halfSize,halfSize,1)
    xIn.astype(float)
    yIn.astype(float)
    x,y=numpy.meshgrid(xIn,yIn)
    r=numpy.sqrt(x**2+y**2)
    #avoid divide by zero issues
    y[y==0]=numpy.finfo(numpy.float).eps
    xOverY=x/y
    theta = numpy.arctan(xOverY)
    theta[halfSize+1,halfSize+1]=0

    #number of wedges (pairs!!)--eventually to be a var passed in
    nWedges=scanDict['numWedges']#8.0
    #number of ring pairs
    #nRings=15.0
#    ringWidth = 2.0/nRings
    ringWidth=scanDict['ringWidth']
    nRings=2.0/ringWidth
    #width of wedges in radians
    wedgeWidth = 2.0*math.pi/nWedges
    #ring function--describes how the ring width increases with eccentricity
    ringFunction=numpy.power(r/halfSize,0.3)+0.2#um, is there an int float problem here?

    wedgeMask = 0.5 - (numpy.mod(theta,wedgeWidth)>(wedgeWidth/2.0)) #does this work
    rmA=numpy.mod(ringFunction,ringWidth)>(ringWidth/2.0)
    ringMask = 1 - 2.0*(rmA)

    checkerBoardLogic=wedgeMask*ringMask + 0.5
    #initialize an array of 1024x1024x3 for RGB channels
    checkerBoardA=numpy.ones((imageSize, imageSize,3))
    checkerBoardAR=numpy.ones((imageSize, imageSize))
    checkerBoardAB=numpy.ones((imageSize, imageSize))
    checkerBoardAG=numpy.ones((imageSize, imageSize))
    #set the RGB values based on the colors passed in during launch
    #CBA, logic=1-->colorB, logic=0-->colorA
    #CBB, logic=1-->colorA, logic=0-->colorB
    #color A, column 1
    checkerBoardAR[checkerBoardLogic==1] = colorAp[0]
    checkerBoardAG[checkerBoardLogic==1] = colorAp[1]
    checkerBoardAB[checkerBoardLogic==1] = colorAp[2]
    checkerBoardAR[checkerBoardLogic==0] = colorBp[0]
    checkerBoardAG[checkerBoardLogic==0] = colorBp[1]
    checkerBoardAB[checkerBoardLogic==0] = colorBp[2]
    #now add in the background color around the widest ring
#    imageMask=numpy.ones((imageSize,imageSize))
 #   imageMask[r>halfSize]=-1
    checkerBoardAR[r>halfSize]=colorBGp[0]
    checkerBoardAG[r>halfSize]=colorBGp[1]
    checkerBoardAB[r>halfSize]=colorBGp[2]
    #smoosh the arrays together
    checkerBoardA[:,:,0]=checkerBoardAR
    checkerBoardA[:,:,1]=checkerBoardAG
    checkerBoardA[:,:,2]=checkerBoardAB

    checkerBoardB=numpy.ones((imageSize, imageSize,3))
    checkerBoardBR=numpy.ones((imageSize, imageSize))
    checkerBoardBB=numpy.ones((imageSize, imageSize))
    checkerBoardBG=numpy.ones((imageSize, imageSize))
    checkerBoardBR[checkerBoardLogic==1] = colorBp[0]
    checkerBoardBG[checkerBoardLogic==1] = colorBp[1]
    checkerBoardBB[checkerBoardLogic==1] = colorBp[2]
    checkerBoardBR[checkerBoardLogic==0] = colorAp[0]
    checkerBoardBG[checkerBoardLogic==0] = colorAp[1]
    checkerBoardBB[checkerBoardLogic==0] = colorAp[2]
    checkerBoardBR[r>halfSize]=colorBGp[0]
    checkerBoardBG[r>halfSize]=colorBGp[1]
    checkerBoardBB[r>halfSize]=colorBGp[2]
    checkerBoardB[:,:,0]=checkerBoardBR
    checkerBoardB[:,:,1]=checkerBoardBG
    checkerBoardB[:,:,2]=checkerBoardBB
    #finally, create the image textures!!
    #oooh, these are fun--tiles the checkerboards!
    #stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize)
    #stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize)
    stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize,sf=1/imageSize,units='pix',texRes=imageSize)
    stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize,sf=1/imageSize,units='pix')


    ReverseFreq =flickFreq #drift in Hz. could be an input param eventually?


    #make a fixation cross which will rotate 45 deg on occasion
    if fixColorChange==1:
        fixColorOrig=[1,1,1]
        fixColorNew=[1,-1,-1]
    else:
        fixColorOrig=[-1,-1,-1]
        fixColorNew=[-1,-1,-1]
    fix0 = visual.Circle(winSub,radius=IR,edges=32,lineColor=gray,lineColorSpace='rgb',
            fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.4),(0.0,0.4)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)

    fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.4,0.0),(0.4,0.0)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)
    msg1x=visual.TextStim(winSub, pos=[0,+8],text='flickering checkerboard, asymmetric timing')
    msg1a = visual.TextStim(winSub, pos=[0,+5],text='During the scan, please keep your eyes on the + in the center.',height=1)
    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Hit any button any time the + becomes an X.',height=1)
    msg1=visual.TextStim(winSub,pos=[0,-3],text='Subject: Hit a button when ready.',color=[1,-1,-1],colorSpace='rgb')
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
    responseKeys=list(scanDict['subjectResponse'])
    responseKeys.extend('q')
    responseKeys.extend('escape')
    while thisKey==None:
        thisKey = event.waitKeys(keyList=responseKeys)
    if thisKey in ['q','escape']:
        core.quit() #abort
    else:
        event.clearEvents()
    responseKeys=list(scanDict['subjectResponse'])

    msg1a = visual.TextStim(winSub, pos=[0,+5],text='   ',height=1)
    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Waiting for magnet',height=1)
    msg1a.draw()
    msg1b.draw()
    fix0.draw()
    fix1.draw()
    fix2.draw()
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

    #draw the fixation point
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()
    # and drift it
    timeNow = scanTimer.getTime()
    if screenCount==2:
        msg = visual.TextStim(winOp,units='pix',pos=(0.0,200.0),text = 't = %.3f' %timeNow)
        msg.draw()
        #create subject response messages
        msgRespRecent=visual.TextStim(winOp,pos=[0,0],units='pix',text='',height=40)
        msgResponse=visual.TextStim(winOp,pos=[0,-200],units='pix',text='',height=40)
    loopCounter=0
    restLoopCounter=0
    TrCounter=0
    if timeBase==0:
        ttp=TrCounter+1
        if screenCount==2:
            msgTr=visual.TextStim(winOp,units='pix',pos=(0.0,200.0),text='Tr = %i' %ttp)
            msgTr.draw()
    # msg4 = visual.TextStim(operatorWindow,units='pix',text = 'percent correct',pos=(0.0,-10),height=2)
    # msg4.draw()
    # msg5 = visual.TextStim(operatorWindow,units='pix',text = 'time since correct',pos=(0.0,-15),height=2)
    # msg5.draw()


    fixTimer=core.Clock()
    respTimer=core.Clock()
    flickerTimer=core.Clock()

    fixOri=0
    numCoins=0
    event.clearEvents()
    for key in event.getKeys():
        if key in ['q','escape']:
            core.quit()
        elif key in responseKeys and respTimeCheck<respDuration:
            subjectResponse[numCoins]=1
    #time based loop advancement

    respCounter=0

    #display rest for pre-scan duration
    while timeNow<scanDict['preScanRest']:
        timeNow = scanTimer.getTime()
        #draw fixation
        #every 100 frames, decide if the fixation point should change or not
        if restLoopCounter%100 ==0 and restLoopCounter>10:
            #flip a coin to decide
            flipCoin=numpy.random.ranf()
            if flipCoin<fixPercentage:
                #reset timers/change ori
                fixOri=45
                #change colors if also asked for
                if fixColorChange==1:
                    fix1.setLineColor(fixColorNew)
                    fix1.setFillColor(fixColorNew)
                    fix2.setLineColor(fixColorNew)
                    fix2.setFillColor(fixColorNew)
                fixTimer.reset()
                respTimer.reset()
                numCoins+=1
                subjectResponse[numCoins]=0
            #store info--expected response or not?
            respCounter+=1
            subRespArray[respCounter,0]=timeNow
            subRespArray[respCounter,1]=flipCoin<fixPercentage
        fixTimeCheck=fixTimer.getTime()
        respTimeCheck=respTimer.getTime()
        if fixTimeCheck >fixDuration: #timer expired--reset ori
            fixOri=0
            fix1.setLineColor(fixColorOrig)
            fix1.setFillColor(fixColorOrig)
            fix2.setLineColor(fixColorOrig)
            fix2.setFillColor(fixColorOrig)

        fix1.setOri(fixOri)
        fix2.setOri(fixOri)
        fix0.draw()
        fix1.draw()
        fix2.draw()
        winSub.flip()
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in responseKeys and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1
                plotResp[numCoins]=1
                subRespArray[respCounter,2]=1
            #update the operator on subject responses
            if screenCount==2:
                msg.setText('t = %.3f' %timeNow)
                msg.draw()
                if numCoins>10:
                    findRespRecent=subjectResponse[numCoins-10:numCoins]
                    calcRespRecent=findRespRecent[findRespRecent==1]
                    numCorrectRecent=float(calcRespRecent.shape[0])
                    pctCorRecent=100.0*float(numCorrectRecent)/(10.0)
                    msgRespRecent.setText('last 10 responses %.1f %% correct' %pctCorRecent)
                    msgRespRecent.draw()
                if numCoins>1:
                    findResp=subjectResponse[~numpy.isnan(subjectResponse)]
                    calcResp=findResp[findResp==1]
                    numCorrect=float(calcResp.shape[0])
                    pctCorrect=100.0*float(numCorrect)/(float(numCoins))
                    msgResponse.setText('All responses %.1f %% correct' %pctCorrect)
                    msgResponse.draw()
                winOp.flip()
                blank.draw()


    #pre-scan rest is done.
    #prepare for looping through the cycles
    epochTimer = core.Clock()

    currentStim=blank
    #time based looping through stimulus
    while timeNow<startTime+scanLength: #loop until total scan duration has elapsed
        timeBefore = timeNow
        timeNow = scanTimer.getTime()
        deltaT=timeNow - startTime
        deltaTinc=timeNow-timeBefore
        #update the operator on subject responses
        if screenCount==2:
            if numCoins>10:
                findRespRecent=subjectResponse[numCoins-10:numCoins]
                calcRespRecent=findRespRecent[findRespRecent==1]
                numCorrectRecent=float(calcRespRecent.shape[0])
                pctCorRecent=100.0*float(numCorrectRecent)/(10.0)
                msgRespRecent.setText('last 10 responses %.1f %% correct' %pctCorRecent)
                msgRespRecent.draw()
            if numCoins>1:
                findResp=subjectResponse[~numpy.isnan(subjectResponse)]
                calcResp=findResp[findResp==1]
                numCorrect=float(calcResp.shape[0])
                pctCorrect=100.0*float(numCorrect)/(float(numCoins))
                msgResponse.setText('All responses %.1f %% correct' %pctCorrect)
                msgResponse.draw()
            msg.setText('t = %.3f' %timeNow)
            msg.draw()
            winOp.flip()
            currentStim.draw()

        #every 100 frames, decide if the fixation point should change or not
        if loopCounter%100 ==0 and loopCounter>10:
            #flip a coin to decide
            flipCoin=numpy.random.ranf()
            if flipCoin<fixPercentage:
                #reset timers/change ori
                fixOri=45
                #change colors if also asked for
                if fixColorChange==1:
                    fix1.setLineColor(fixColorNew)
                    fix1.setFillColor(fixColorNew)
                    fix2.setLineColor(fixColorNew)
                    fix2.setFillColor(fixColorNew)
                fixTimer.reset()
                respTimer.reset()
                numCoins+=1
                subjectResponse[numCoins]=0
            #store info--expected response or not?
            respCounter+=1
            subRespArray[respCounter,0]=timeNow
            subRespArray[respCounter,1]=flipCoin<fixPercentage
        fixTimeCheck=fixTimer.getTime()
        respTimeCheck=respTimer.getTime()
        if fixTimeCheck >fixDuration: #timer expired--reset ori
            fixOri=0
            fix1.setLineColor(fixColorOrig)
            fix1.setFillColor(fixColorOrig)
            fix2.setLineColor(fixColorOrig)
            fix2.setFillColor(fixColorOrig)

        fix1.setOri(fixOri)
        fix2.setOri(fixOri)

        # display stimulus for stimDuration time, then rest for restDuration time
        epochTime=epochTimer.getTime()
        # epoch of stimulus
        if epochTime<scanDict['stimDuration']:
            #alternate wedge 1&2 at flicker rate
            flickerTimeCheck = flickerTimer.getTime()
            if flickerTimeCheck<1/(2.0*ReverseFreq):
                #first half of a period, show wedge 1
                #image1.draw()
                stimA.draw()
                currentStim=stimA
            elif flickerTimeCheck<1/ReverseFreq:
                #second half of period, show wedge 2
#                image2.draw()
                 stimB.draw()
                 currentStim=stimB
            else:
                #clocked over, reset timer
                #could also do some modulus of timing
                flickerTimer.reset()
            fix0.draw()
            fix1.draw()
            fix2.draw()
        elif epochTime<scanDict['period']:
            #rest for REMAINDER of full period (restDuration implicit)
            fix0.draw()
            fix1.draw()
            fix2.draw()
            currentStim=blank
        else:
            epochTimer.reset()

        winSub.flip()

        #count number of keypresses since previous frame, break if non-zero
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in responseKeys and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1
                subRespArray[respCounter,2]=1

        loopCounter +=1
#        print(loopCounter)

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
    outFile='flickerArbResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    winSub.close()
    if screenCount==2:
        winOp.close()
