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
from pylab import *

#############################################################################
################### rings ###################################
#############################################################################

def ringScan(scanDict, screenSize=[1024,768], direction = 1.0):
    #do ring
    scanLength = float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    if scanDict['operatorScreen']==scanDict['subjectScreen']:
        screenCount=1
    else:
        screenCount=2
    thisPlatform=scanDict['platform']
    #if there is only one window, need to display the winOp stuff and then clear it
    screenSize=scanDict['screenSize']
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
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units='deg',screen=scanDict['subjectScreen'],
                       color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=False,allowGUI=False)

    #parse out vars from scanDict
    IR=scanDict['innerRadius']
    OR=scanDict['outerRadius']
    #get actual size of window--useful in the functions
    subWinSize=winSub.size
    screenSize=numpy.array([subWinSize[0],subWinSize[1]])
    fixPercentage = scanDict['fixFraction']
    dutyCycle=scanDict['dutyCycle']
    fixDuration = 0.2
    respDuration = 1.0
    dummyLength=int(numpy.ceil(scanLength*60/100))
    subjectResponse=numpy.zeros(( dummyLength,1))
    subjectResponse[:]=numpy.nan
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black = [-1.0,-1.0,-1.0]
    gridgray=[0.25,0.25,0.25]
    numRadialCycles = 0.75/1.2
    numAngularCycles = 4.0
    wedgeEdges = numpy.linspace(0.0,360.0,9)
    ringOri = 0.0

    #figure out the ring sizes
    #start with a fixed width ring, given by the duty cycle.
    #this is a percentage of the total size
    maxWidth=(OR-IR)*dutyCycle/100.0
    width=maxWidth
    #print "maxWidth" ,maxWidth
    #assign starting IR and OR for the actual ring
    ringIR=IR
    ringOR=ringIR+maxWidth
    #set the amplitude of the ring for the sawtooth function
    ringAmp=OR-IR-maxWidth
    #print 'ringAmp', ringAmp
    #print 'OR', OR
    #print 'IR', IR
    quitKeys=['q','escape']
    radialUnits = 2.0
    debugVar=numpy.zeros((  int(scanLength*60) ,9))
    ringRate = (OR - (IR+width))/scanDict['period']
    contrast=scanDict['contrast']
#    ringRadPhi=numpy.zeros((8,1))
#    ringRadPhiInit=numpy.zeros((8,1))
    ringRadPhiInit=numpy.random.rand(8)
    ringRadPhi=ringRadPhiInit
#    for iP in range(8):
#        ringRadPhiInit[iP]=numpy.random.random()*2.0*math.pi


    startOR = OR - scanDict['preScanRest']*ringRate
    #needs to be direction based?

    ring1 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[0],wedgeEdges[8]), radialPhase = ringRadPhiInit[0],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring2 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[1],wedgeEdges[8]), radialPhase = ringRadPhiInit[1],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring3 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge =(wedgeEdges[2],wedgeEdges[8]), radialPhase = ringRadPhiInit[2],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring4 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[3],wedgeEdges[8]), radialPhase = ringRadPhiInit[3],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring5 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[4],wedgeEdges[8]), radialPhase = ringRadPhiInit[4],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring6 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[5],wedgeEdges[8]), radialPhase = ringRadPhiInit[5],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring7 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[6],wedgeEdges[8]), radialPhase = ringRadPhiInit[6],
                              contrast=contrast, interpolate=False, autoLog=False)
    ring8 = visual.RadialStim(winSub,pos=[0,0],tex='sqrXsqr',radialCycles = numRadialCycles*OR*radialUnits,
                              angularCycles = numAngularCycles,angularPhase=0,size=startOR*radialUnits,color=1,
                              visibleWedge = (wedgeEdges[7],wedgeEdges[8]), radialPhase = ringRadPhiInit[7],
                              contrast=contrast, interpolate=False, autoLog=False)
    #create a gray circle to mask the inside of the radialStim
    ringMask=visual.Circle(winSub,radius=startOR-width,edges=32,lineColor=gray, lineColorSpace='rgb',
                           fillColor=gray,fillColorSpace='rgb',autoLog=False,units='deg',opacity=1.0)



    #try a new mask
    mask=numpy.zeros(( int(OR*100),1))
    ringRadPhiDelta=ringRadPhiInit
    #driftFreq = 0.2 #Hz after L&H
    driftFreq = scanDict['animFreq']
    driftReverseFreq = 1.0 #Hz


    fix0=visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
                       fillColor=gray,fillColorSpace='rgb',autoLog=False,units='deg')
    fix1 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',
                            fillColor=black,fillColorSpace='rgb',autoLog=False,units='deg')
    fix2 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((-0.15,0),(0.15,0.0)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',autoLog=False,units='deg')
    #add to the fixation with a faint background polar grid
    gridRadii=numpy.zeros((8,1))
    gridRadii[0]=IR
    gridRadii[1]=2*IR
    gridRadii[2]=4*IR
    gridRadii[3]=6*IR
    gridRadii[4]=8*IR
    gridRadii[5]=16*IR
    gridRadii[6]=32*IR
    gridRadii[7]=OR
    gridCircle=visual.Circle(winSub,radius=gridRadii[0],edges=128,lineColor=gridgray,lineColorSpace='rgb',autoLog=False)
    gridEnds=numpy.zeros((8,2))
    gridEnds[0,0]=0
    gridEnds[0,1]=OR
    gridEnds[1,0]=OR
    gridEnds[1,1]=OR
    gridEnds[2,0]=OR
    gridEnds[2,1]=0
    gridEnds[3,0]=OR
    gridEnds[3,1]=-OR
    gridEnds[4,0]=0
    gridEnds[4,1]=-OR
    gridEnds[5,0]=-OR
    gridEnds[5,1]=-OR
    gridEnds[6,0]=-OR
    gridEnds[6,1]=0
    gridEnds[7,0]=-OR
    gridEnds[7,1]=OR
    gridSpoke=visual.Line(winSub,start=(0,0),end=(0,OR),lineColor=gridgray,lineColorSpace='rgb',autoLog=False)

    if direction==1:
        scanNameText='contracting ring, %2.1f%% duty cycle' %dutyCycle
    else:
        scanNameText='expanding ring, %2.1f%% duty cycle' %dutyCycle

    #wait for subject
    msg1=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msg1.draw()
    winSub.flip()
    thisKey=None
    responseKeys=list(scanDict['subjectResponse'])
    responseKeys.extend('q')
    responseKeys.extend('escape')
    while thisKey==None:
        thisKey = event.waitKeys(keyList=responseKeys)
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

    #draw the stimulus
#    ring1.draw()
#    ring2.draw()
#    ring3.draw()
#    ring4.draw()
#    ring5.draw()
#    ring6.draw()
#    ring7.draw()
#    ring8.draw()
#    ringMask.draw()
    if thisPlatform<3:
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[0])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[1])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[2])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[3])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[4])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[5])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[6])
        gridCircle.draw()
        gridCircle.setRadius(gridRadii[7])
        gridCircle.draw()
        gridSpoke.setEnd(gridEnds[0,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[1,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[2,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[3,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[4,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[5,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[6,])
        gridSpoke.draw()
        gridSpoke.setEnd(gridEnds[7,])
        gridSpoke.draw()
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
    fixOri=0
    numCoins=0
    phaseSign=1.0
    phaseTimer = core.Clock()
    event.clearEvents()



    #drift it
    while timeNow<startTime+scanLength:
        timeBefore = timeNow #seems to be OK--testing shows it doesn't alias
        timeNow = scanTimer.getTime()
        deltaT=timeNow-startTime
        modDeltaT = (deltaT+scanDict['preScanRest'])%scanDict['period']
        deltaTinc=timeNow-timeBefore
        thisWidth=width*math.log(ringOR)
        thisWidth=width

        #fix time to account for preScanRest. Add on the fractional period requested
        deltaTshift=deltaT+(scanDict['period'] -scanDict['preScanRest'])
        #new way to calculate the OR, based on the formula for a sawtooth
        #calculate the new OR for this timestep
        #from wikipedia
        #yWikiTrig=(-2*amplitude/pi)*atan(cot(pi*t/period));
        #yT2=0.5*(yWikiTrig+amplitude);

        if direction<0:
            #expanding
            ringIR=IR +0.5*(ringAmp + (-2.0*ringAmp/math.pi)*numpy.arctan(1.0/numpy.tan(math.pi*deltaTshift/scanDict['period'])))
        else:
            #contracting
            ringIR=IR+0.5*(ringAmp - (-2.0*ringAmp/math.pi)*numpy.arctan(1.0/numpy.tan(math.pi*deltaTshift/scanDict['period'])))
        ringOR=ringIR+thisWidth
#        debugVar[loopCounter,0]=deltaT
#        debugVar[loopCounter,1]=ringIR
#        debugVar[loopCounter,2]=ringOR



        #set the ORs
        ring1.setSize(ringOR*radialUnits)
        ring1.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring2.setSize(ringOR*radialUnits)
        ring2.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring3.setSize(ringOR*radialUnits)
        ring3.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring4.setSize(ringOR*radialUnits)
        ring4.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring5.setSize(ringOR*radialUnits)
        ring5.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring6.setSize(ringOR*radialUnits)
        ring6.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring7.setSize(ringOR*radialUnits)
        ring7.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ring8.setSize(ringOR*radialUnits)
        ring8.setRadialCycles(ringOR*radialUnits*numRadialCycles)
        ringMask.setRadius(ringIR)
        #experimental mask
#        mask[0:ringIR*100]=0.5
#        mask[ringIR*100:ringOR*100]=1
#        mask[ringOR*100:]=0
#        ring1.setMask(mask)
#        ring2.setMask(mask)
#        ring3.setMask(mask)
#        ring4.setMask(mask)
#        ring5.setMask(mask)
#        ring6.setMask(mask)
#        ring7.setMask(mask)
#        ring8.setMask(mask)

        #new phase
        #ringRadPhi = driftFreq*deltaT
#        ringRadPhi = ringRadPhi + 2.0*math.pi*driftFreq*(timeNow-timeBefore)
        #new direction of phase drift--set randomly but not too often
#        phaseTimeCheck = phaseTimer.getTime()
##        debugVar[loopCounter,3]=phaseTimeCheck
#        phaseCoin=numpy.random.ranf()
#        if phaseCoin<1.0 and phaseTimeCheck>3.0:
#            phaseTimer.reset()
#            phaseSign *= -1.0
         #set the phase
#        ring1.setRadialPhase(ringRadPhi*phaseSign)
#        ring2.setRadialPhase(-1.0*ringRadPhi*phaseSign)
#        ring3.setRadialPhase(ringRadPhi*phaseSign)
#        ring4.setRadialPhase(-1.0*ringRadPhi*phaseSign)
#        ring5.setRadialPhase(ringRadPhi*phaseSign)
#        ring6.setRadialPhase(-1.0*ringRadPhi*phaseSign)
#        ring7.setRadialPhase(ringRadPhi*phaseSign)
#        ring8.setRadialPhase(-1.0*ringRadPhi*phaseSign)


        setSign=math.floor(driftReverseFreq*deltaT/3.0)
        if setSign%2==0:
            phaseSign=1.0
        else:
            phaseSign=-1.0
        ringRadPhiDelta = driftFreq*deltaTinc
        ringRadPhi[0] += ringRadPhiDelta*phaseSign
        ringRadPhi[1] += ringRadPhiDelta*phaseSign*-1
        ringRadPhi[2] += ringRadPhiDelta*phaseSign
        ringRadPhi[3] += ringRadPhiDelta*phaseSign*-1
        ringRadPhi[4] += ringRadPhiDelta*phaseSign
        ringRadPhi[5] += ringRadPhiDelta*phaseSign*-1
        ringRadPhi[6] += ringRadPhiDelta*phaseSign
        ringRadPhi[7] += ringRadPhiDelta*phaseSign*-1
        ring1.setRadialPhase(ringRadPhiInit[0])
        ring2.setRadialPhase(ringRadPhi[1])
        ring3.setRadialPhase(ringRadPhi[2])
        ring4.setRadialPhase(ringRadPhi[3])
        ring5.setRadialPhase(ringRadPhi[4])
        ring6.setRadialPhase(ringRadPhi[5])
        ring7.setRadialPhase(ringRadPhi[6])
        ring8.setRadialPhase(ringRadPhi[7])
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


        fix1.setOri(fixOri)
        fix2.setOri(fixOri)

        ring1.draw()
        ring2.draw()
        ring3.draw()
        ring4.draw()
        ring5.draw()
        ring6.draw()
        ring7.draw()
        ring8.draw()
        ringMask.draw()
        #draw grid only if NOT linux, where it looks bad....
        if thisPlatform<3:
            gridCircle.setRadius(gridRadii[0])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[1])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[2])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[3])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[4])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[5])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[6])
            gridCircle.draw()
            gridCircle.setRadius(gridRadii[7])
            gridCircle.draw()
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[0,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[1,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[2,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[3,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[4,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[5,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[6,])
            gridSpoke.draw()
            gridSpoke.setEnd(gridEnds[7,])
            gridSpoke.draw()
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

    #summarize responses
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

    #numpy.savetxt('debug.txt',debugVar,fmt='%.3f')
    #create an output file in a subdirectory
    #check for the subdirectory
    if os.path.isdir('subjectResponseFiles')==False:
        #create directory
        os.makedirs('subjectResponseFiles')
    nowTime=datetime.datetime.now()
    outFile='ringResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    if screenCount==2:
        winOp.close()
    winSub.close()
