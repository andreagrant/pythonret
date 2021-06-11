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
################### rings ###################################
#############################################################################

def ringScan(scanDict, screenSize=[1024,768], direction = 1.0):
    #do ring
    scanLength = float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'],
                       color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=True,allowGUI=False)
    winOp = visual.Window([500,200],monitor='testMonitor',units='deg',screen=scanDict['operatorScreen'],
                          color=[0.0,0.0,0.0],colorSpace='rgb')

    msgScanLength=visual.TextStim(winOp,pos=[0,2],text='Scan length (s): %.1f' %scanLength)
    msgScanTr=visual.TextStim(winOp,pos=[0,1],units='deg',height=0.8,text='No. of Volumes (at Tr=%.2f): %.0f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
    msgScanLength.draw()
    msgScanTr.draw()
    winOp.flip()
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
    gridgray=[0.5,0.5,0.5]
    numRadialCycles = 0.75/1.2
    numAngularCycles = 4.0
    wedgeEdges = numpy.linspace(0.0,360.0,9)
    ringOri = 0.0
    ringIR = OR*(1-dutyCycle/100.0)
    #WORKING HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    ringOR=OR
    width=ringOR-ringIR
    quitKeys=['q','escape']
    respKeys=['r','g','b','y','1','2','3','4']
    radialUnits = 2.0
    debugVar=numpy.zeros((scanLength*60,9))
    ringRate = (OR - (IR+width))/scanDict['period']
    contrast=scanDict['contrast']
#    ringRadPhi=numpy.zeros((8,1))
#    ringRadPhiInit=numpy.zeros((8,1))
    ringRadPhiInit=numpy.random.rand(8)
    ringRadPhi=ringRadPhiInit
#    for iP in range(8):
#        ringRadPhiInit[iP]=numpy.random.random()*2.0*math.pi


    startOR = OR - scanDict['preScanRest']*ringRate


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
                           fillColor=gray,fillColorSpace='rgb',autoLog=False)
    ringRadPhiDelta=ringRadPhiInit
    #driftFreq = 0.2 #Hz after L&H
    driftFreq = scanDict['animFreq']
    driftReverseFreq = 1.0 #Hz


    fix0=visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
                       fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',
                            fillColor=black,fillColorSpace='rgb',autoLog=False)
    fix2 = visual.ShapeStim(winSub,pos=[0.0,0.0],vertices=((-0.15,0),(0.15,0.0)),lineWidth=3.0,
                            lineColor=black,lineColorSpace='rgb',autoLog=False)

    #add to the fixation with a faint background polar grid
    gridRadii=numpy.zeros((5,1))
    gridRadii[0]=IR
    gridRadii[1]=2*IR
    gridRadii[2]=4*IR
    gridRadii[3]=6*IR
    gridRadii[4]=8*IR
    gridCircle=visual.Circle(winSub,radius=gridRadii[0],edges=32,lineColor=gridgray,lineColorSpace='rgb',autoLog=False)
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

    print(dutyCycle)
    if direction==1:
        scanNameText='contracting ring, %2.1f%% duty cycle' %dutyCycle
    else:
        scanNameText='expanding ring, %2.1f%% duty cycle' %dutyCycle

    #wait for subject
    msg1=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msg1.draw()
    winSub.flip()
    thisKey=None
    while thisKey==None:
        thisKey = event.waitKeys(keyList=['r','g','b','y','1','2','3','4','q','escape'])
    if thisKey in quitKeys:
        core.quit()
    else:
        event.clearEvents()

    #wait for trigger
    msg1.setText('Noise Coming....')
    msg1.draw()
    winSub.flip()
    trig=None
    while trig==None:
        trig=event.waitKeys(keyList=['t','5','q','escape'])
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
    gridCircle.draw()
    gridCircle.setRadius(gridRadii[1])
    gridCircle.draw()
    gridCircle.setRadius(gridRadii[2])
    gridCircle.draw()
    gridCircle.setRadius(gridRadii[3])
    gridCircle.draw()
    gridCircle.setRadius(gridRadii[4])
    gridCircle.draw()
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
    timeMsg = visual.TextStim(winOp,pos=[0,-1],text = 't = %.3f' %timeNow)
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
        #TO DO--make the width a function of the eccentricity
        ringMid=(ringOR+ringIR)/2.0
        thisWidth=width*math.log(ringMid)
        if direction>0:
            #new OR--moves total eccentricity cycle in 24 (the period)
            # the outside goes from OR to IR+width, or 5.8-0.4+1.2
            ringOR = OR - modDeltaT*ringRate
            #new IR
            ringIR = OR - width - modDeltaT*ringRate
        else:
            ringOR = IR + width + modDeltaT*ringRate
            ringIR = IR + modDeltaT*ringRate
        #set them
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
        debugVar[loopCounter,0]=deltaT
        debugVar[loopCounter,1]=deltaTinc
        debugVar[loopCounter,2]=ringRadPhiDelta
        debugVar[loopCounter,3]=ringRadPhi[0]
        debugVar[loopCounter,4]=ringRadPhi[1]
#        debugVar[loopCounter,0]=deltaT
#        debugVar[loopCounter,1]=ringRadPhi
 #        debugVar[loopCounter,2]=ringIR
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
        timeMsg.setText('t = %.3f' %timeNow)
        timeMsg.draw()
        msgScanLength.draw()
        msgScanTr.draw()
        winSub.flip()
        winOp.flip()

        #look for responses
        for key in event.getKeys():
            if key in quitKeys:
                core.quit()
            elif key in respKeys and respTimeCheck<respDuration:
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
    msg1=visual.TextStim(winSub,pos=[0,+3],text=msgText)
    msg1.draw()
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
    winOp.close()
    winSub.close()
