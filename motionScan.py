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
################### MT localizer ###################################
#############################################################################


def motionScan(scanDict, screenSize=[1024,768], dotSpeed=5.8, dotMotion='radial',direction = 1.0):
    scanLength = float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    #get actual size of window--useful in the functions
    #count number of screens
    if scanDict['operatorScreen']==scanDict['subjectScreen']:
        screenCount=1
    else:
        screenCount=2
    screenSize=scanDict['screenSize']
    thisPlatform=scanDict['platform']
    #if there is only one window, need to display the winOp stuff and then clear it
    #second window is deeply damanged in 1.79. Thought it was the aperture, but it's also the element stim I think
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

    #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units='deg',screen=scanDict['subjectScreen'],
                       color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=False,allowGUI=False)
    subWinSize=winSub.size
        #parse out vars from scanDict
    IR=scanDict['innerRadius']
    OR=scanDict['outerRadius']
    screenSize=numpy.array([subWinSize[0],subWinSize[1]])
    fixPercentage=scanDict['fixFraction']
    fixDuration=0.2
    respDuration=1.0
    dummyLength=int(numpy.ceil(scanLength*60/100))
    subjectResponse=numpy.zeros((dummyLength,1))
    subjectResponse[:]=numpy.nan
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]
    numDots=700
    dotSize=0.1 #deg
    #dotAperture=OR
    frameRate=60.0
    quitKeys=['q','escape']
    #OR+=1

    dummyVar=0
    #following startfield.py demo
    #dot locations
    dotsPolarAngle = numpy.random.rand(numDots)*360
    dotsRadius = (numpy.random.rand(numDots)**0.5)*OR
    numpy.savetxt('rads.txt',dotsRadius,fmt='%.1f')
    numpy.savetxt('pols.txt',dotsPolarAngle,fmt='%.1f')
    dotsDirection = numpy.random.rand(numDots)*2.0*math.pi

    #make an aperture mask
#    ap = visual.Aperture(winSub,size=(OR-1)*2.0 ,units='deg')
    #ap = visual.Aperture(winSub,size=(OR-1) ,units='deg')
    #ap.disable()
    #create the dots
    #color is based on contrast--not sure this is quite how I want it?
    # if contrast is 0, dot color is 0 which = background
    # if contrast is 1, dot color is 1, which is white, which is the "full" contrast...
    dotContrast=[scanDict['contrast'],scanDict['contrast'],scanDict['contrast']]
    movingDots = visual.ElementArrayStim(winSub, units='deg',fieldShape='circle',
                                         nElements=numDots, sizes=dotSize,
                                         elementMask = 'circle',colors=dotContrast)
    #move them into initial position
    dotsX, dotsY = misc.pol2cart(dotsPolarAngle,dotsRadius)
    numpy.savetxt('dotx.txt',dotsX,fmt='%.1f')
    numpy.savetxt('doty.txt',dotsY,fmt='%.1f')
    #dotsX *= 0.75 #aspect ratio issue
    movingDots.setXYs(numpy.array([dotsX, dotsY]).transpose())


    #fixation
    fix0=visual.Circle(winSub,radius=IR,edges=32,lineColor=gray,lineColorSpace='rgb',
                       fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',
                            fillColor=black,fillColorSpace='rgb',autoLog=False)
    fix2 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((-0.15,0),(0.15,0.0)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',autoLog=False)

    #wait for subject
    if direction==1:
        scanNameText='motion localizer. On condition is %s dots' % ('moving')
    else:
        scanNameText='motion localizer. On condition is %s dots' % ('static')

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
    #ap.enable()
    #draw the stimulus
    #winSub.setColor(black)
    movingDots.draw()
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()

    #draw the time
    timeNow=scanTimer.getTime()
    #timeMsg=visual.TextStim(winSub,pos=[-screenSize[0]/2+100,-screenSize[1]/2+15],units='pix',text= 't = %.3f' %timeNow)
#    timeMsg = visual.TextStim(winOp,pos=[0,-1],text = 't = %.3f' %timeNow)
#    timeMsg.draw()

    #print(timeNow)
    loopCounter=0
    fixTimer=core.Clock()
    respTimer=core.Clock()
    flipTimer=core.Clock()
    fixOri=0
    numCoins=0
    epochTimer = core.Clock()
    miniEpochTimer=core.Clock()
    event.clearEvents()


    #pre-scan stimulus


    #let's make a kind of phase variable that I can adjust for pre-scan rest
    phaseInit=0
    #need a kind of phase variable to dial back (rather, advance it up through part of a period)
    phaseInit=scanDict['period']-scanDict['preScanRest']%scanDict['period']

    #drift it
    while timeNow<startTime+scanLength:
        timeBefore=timeNow#um, is this aliasing?
        timeNow=scanTimer.getTime()
        deltaT=timeNow-timeBefore
        runningT=timeNow-startTime
        phase=phaseInit+timeNow
        mode=phase%scanDict['period']

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
        epochTime=epochTimer.getTime()
        miniEpochTime=miniEpochTimer.getTime()

        #every 2 seconds, change the direction of some dots
        if loopCounter%60==0 and loopCounter>10:
            #change direction of 30% of the dots
            flipCoinDots=numpy.random.rand(numDots)
            flippedDots = flipCoinDots>0.3
            numFlipped=numpy.sum(flippedDots)
            dotsDirection[flippedDots] = numpy.random.rand(numFlipped)*2.0*math.pi
            flipTimer.reset()

        #12s epoch
#        if epochTime<scanDict['preScanRest']+scanDict['period']/2.0:
        if mode<scanDict['period']/2.0:
            # on condition (first half of period)
            if direction==1:
                #moving dots for ON CONDITION
                #update dot positions, but keep them inside the radius!
                dotsX = dotsX + dotSpeed*deltaT*numpy.cos(dotsDirection)
                dotsY = dotsY + dotSpeed*deltaT*numpy.sin(dotsDirection)
                lostDots= numpy.square(dotsX)+numpy.square(dotsY) > numpy.square(OR)
                if len(lostDots)>0:
                    #convert to polar coordintates using old position
                    dotsT,dotsR = misc.cart2pol(dotsX[lostDots] - dotSpeed*deltaT*numpy.cos(dotsDirection[lostDots]),
                                                dotsY[lostDots] - dotSpeed*deltaT*numpy.sin(dotsDirection[lostDots]))
                    #flip the direction of motion
                    dotsT +=180
                    #convert back to cartesian coordinates
                    newX,newY = misc.pol2cart(dotsT,dotsR)
                    dotsX[lostDots] = newX
                    dotsY[lostDots]=newY

                movingDots.setXYs(numpy.array([dotsX, dotsY]).transpose())
            else:
                #static dots for ON CONDITION
                if miniEpochTime>1.0:
                    #new field of dots
                    dotsPolarAngle = numpy.random.rand(numDots)*360
                    dotsRadius = (numpy.random.rand(numDots)**0.5)*OR
                    dotsX, dotsY = misc.pol2cart(dotsPolarAngle,dotsRadius)
                    movingDots.setXYs(numpy.array([dotsX, dotsY]).transpose())
                    miniEpochTimer.reset()
#        elif epochTime<scanDict['preScanRest']+scanDict['period']:
        elif mode<scanDict['period']:
            #OFF condition (second half of period)
            if direction==1:
                if miniEpochTime>1.0:
                    #new field of dots
                    dotsPolarAngle = numpy.random.rand(numDots)*360
                    dotsRadius = (numpy.random.rand(numDots)**0.5)*OR
                    dotsX, dotsY = misc.pol2cart(dotsPolarAngle,dotsRadius)
                    movingDots.setXYs(numpy.array([dotsX, dotsY]).transpose())
                    miniEpochTimer.reset()
            else:
                #update dot positions, but keep them inside the radius!
                dotsX = dotsX + dotSpeed*deltaT*numpy.cos(dotsDirection)
                dotsY = dotsY + dotSpeed*deltaT*numpy.sin(dotsDirection)
                lostDots= numpy.square(dotsX)+numpy.square(dotsY) > numpy.square(OR)
                if len(lostDots)>0:
                    #convert to polar coordintates using old position
                    dotsT,dotsR = misc.cart2pol(dotsX[lostDots] - dotSpeed*deltaT*numpy.cos(dotsDirection[lostDots]),
                                                dotsY[lostDots] - dotSpeed*deltaT*numpy.sin(dotsDirection[lostDots]))
                    #flip the direction of motion
                    dotsT +=180
                    #convert back to cartesian coordinates
                    newX,newY = misc.pol2cart(dotsT,dotsR)
                    dotsX[lostDots] = newX
                    dotsY[lostDots]=newY

                movingDots.setXYs(numpy.array([dotsX, dotsY]).transpose())

        else:
            epochTimer.reset()


        fix1.setOri(fixOri)
        fix2.setOri(fixOri)
        #ap.enable()
        movingDots.draw()
        #ap.disable()
        fix0.draw()
        fix1.draw()
        fix2.draw()
#        timeMsg.setText('t = %.3f' %timeNow)
#        timeMsg.draw()
        #msgScanLength.draw()
        #msgScanTr.draw()
        winSub.flip()
#        winOp.flip()

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
    outFile='motionResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
#    winOp.close()
    winSub.close()
