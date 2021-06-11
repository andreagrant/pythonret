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
import pyglet
pyglet.options['shadow_window'] = False

#############################################################################
################### wedges ###################################
#############################################################################

def wedgeScan(scanDict,screenSize=[1024,768], direction = 1.0):
    #do wedge
    #length of scan in s
    scanLength=float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
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
    OR=scanDict['outerRadius']
    width=scanDict['wedgeWidth']
    contrast=scanDict['contrast']
    #get actual size of window--useful in the functions
    subWinSize=winSub.size
    screenSize=numpy.array([subWinSize[0],subWinSize[1]])
    totalWidth = width
    wedgeWidth = totalWidth/3.0
    fixPercentage = scanDict['fixFraction']
    fixDuration=0.2
    respDuration=1.0
    dummyLength=int(numpy.ceil(scanLength*60/100))
    subjectResponse=numpy.zeros(( dummyLength,1))
    subjectResponse[:]=numpy.nan
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]
    gridgray=[0.5,0.5,0.5]
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
    numRadialCycles = OR/2.0

    #initial orientations of wedges
    #first, need starting angle, which is based on preScanRest
    #at beginning of first FULL CYCLE, want to be at right horizon
    #work backwards to find angle
    preDeltaT=scanDict['preScanRest']
    prePhase=direction*preDeltaT*360.0/scanDict['period']

#    wedgeOriInit=numpy.array([270+wedgeWidth/2.0,270-wedgeWidth/2.0,270-3.0*wedgeWidth/2.0])
    wedgeOriInit=numpy.array([90-prePhase-totalWidth/2.0,90-prePhase-totalWidth/6.0,90-prePhase+totalWidth/6.0])
    wedgeOri=numpy.array([0.0,0.0,0.0])
    #for some reason, the wedges are half the radius I'm expecting. Size must mean diameter? So I have to double the OR to get the expected OR
    wedge1 = visual.RadialStim(winSub,pos = [0, 0],tex='sqrXsqr',radialCycles=numRadialCycles,
         angularCycles=0,angularPhase=0,size=2*OR,color=1,visibleWedge=[0,wedgeWidth],
         ori=wedgeOriInit[0],interpolate=False,angularRes=1000,contrast=contrast,
         autoLog=False)
#    wedge2 = visual.RadialStim(winSub,pos = [0, 0],tex='sqrXsqr',radialCycles=numRadialCycles,
#         angularCycles=0,angularPhase=0,size=OR,color=-1,visibleWedge=[0,wedgeWidth],
#         ori=wedgeOriInit[1],interpolate=False,angularRes=1000,
#         autoLog=False)
#    wedge3 = visual.RadialStim(winSub,pos = [0, 0],tex='sqrXsqr',radialCycles=numRadialCycles,
#         angularCycles=0,angularPhase=0,size=OR,color=1,visibleWedge=[0,wedgeWidth],
#         ori=wedgeOriInit[2],interpolate=False,angularRes=1000,
#         autoLog=False)

    #debugVar=numpy.empty((scanLength*60,3))
    #rotationRate = 1.0/scanDict['period'] #revs per sec
    #rotationRate = 360.0/(refreshRate*scanDict['period']) #deg per frame

    #driftFreq =0.2 #drift in Hz. could be an input param eventually?
    driftFreq=scanDict['animFreq']
    driftReverseFreq = 1.0 #Hz
    #drift rate in cycles per frame
    #driftRate=driftFreq/60.0

    #make a fixation cross which will rotate 45 deg on occasion
    fix0 = visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
            fillColor=gray,fillColorSpace='rgb',autoLog=False)
    fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)

    fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.15,0.0),(0.15,0.0)),lineWidth=3.0,
            lineColor=black,lineColorSpace='rgb',
            fillColor=black,fillColorSpace='rgb',autoLog=False)

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


    #stim.setOri(t*rotationRate*360.0)
    #stim.setRadialPhase(driftRate,'+')
    #stim.setPos()#something here
    if direction==1:
        scanNameText='%s rotating wedge, %2.1f degrees' % ('CW',width)
    else:
        scanNameText='%s rotating wedge, %2.1f degrees' % ('CCW',width)

    msg1=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msg1.draw()
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
#    while len(event.getKeys())==0:
#        core.wait(0.05)
#    event.clearEvents()
    msg1=visual.TextStim(winSub,pos=[0,+3],text='Noise coming....')
    msg1.draw()
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

    #draw the stimulus
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
    wedge1.draw()
    wedge1.setOri(wedgeOriInit[1])
    wedge1.draw()
    wedge1.setOri(wedgeOriInit[2])
    wedge1.draw()
    if scanDict['pairWedge']==1:
        wedge1.setOri(wedgeOriInit[0]+180)
        wedge1.draw()
        wedge1.setOri(wedgeOriInit[1]+180)
        wedge1.draw()
        wedge1.setOri(wedgeOriInit[2]+180)
        wedge1.draw()

#    wedge2.draw()
#    wedge3.draw()
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()
    # and drift it
    timeNow = scanTimer.getTime()
    #row=1
#    msg = visual.TextStim(winSub, pos=[-screenSize[0]/2+45,-screenSize[1]/2+15],units='pix',text = 't = %.3f' %timeNow)
    if screenCount==2:
        msg = visual.TextStim(winOp,pos=[0,-0.5],text = 't = %.3f' %timeNow)
        msg.draw()
    loopCounter=0
    fixTimer=core.Clock()
    respTimer=core.Clock()
    fixOri=0
    numCoins=0
    wedgeRadPhi=numpy.random.rand(3)
    event.clearEvents()
    while timeNow<startTime+scanLength: #loop for scan duration
        timeBefore = timeNow
        timeNow = scanTimer.getTime()
        deltaT=timeNow - startTime
        deltaTinc=timeNow-timeBefore
        wedgeOri=wedgeOriInit+(360.0/scanDict['period'])*deltaT*direction
#        wedge1.setOri(wedgeOri[0])
#        wedge2.setOri(wedgeOri[1])
#        wedge3.setOri(wedgeOri[2])
#        wedgeRadPhi=(2.0*math.pi*driftFreq*deltaT)
        wedgeRadPhiDelta=(driftFreq*deltaTinc) #using deltaT b/c add delta phase later
        #set direction of drift--alternate every cycle
        setSign=math.floor(driftReverseFreq*deltaT/3.0)
        if setSign%2==0:
            phaseSign = 1.0
        else:
            phaseSign = -1.0
        wedgeRadPhi[0] += wedgeRadPhiDelta*phaseSign
        wedgeRadPhi[1] += wedgeRadPhiDelta*phaseSign*-1
        wedgeRadPhi[2] += wedgeRadPhiDelta*phaseSign
#        wedge1.setRadialPhase(wedgeRadPhi[0])
#        wedge2.setRadialPhase(wedgeRadPhi[1])
#        wedge3.setRadialPhase(wedgeRadPhi[2])

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
        wedge1.setRadialPhase(wedgeRadPhi[0])
        wedge1.setOri(wedgeOri[0])
        wedge1.draw()
        wedge1.setRadialPhase(wedgeRadPhi[1])
        wedge1.setOri(wedgeOri[1])
        wedge1.draw()
        wedge1.setRadialPhase(wedgeRadPhi[2])
        wedge1.setOri(wedgeOri[2])
        wedge1.draw()
        if scanDict['pairWedge']==1:
            wedge1.setRadialPhase(wedgeRadPhi[0])
            wedge1.setOri(wedgeOri[0]+180)
            wedge1.draw()
            wedge1.setRadialPhase(wedgeRadPhi[1])
            wedge1.setOri(wedgeOri[1]+180)
            wedge1.draw()
            wedge1.setRadialPhase(wedgeRadPhi[2])
            wedge1.setOri(wedgeOri[2]+180)
            wedge1.draw()

#        wedge2.draw()
#        wedge3.draw()
        fix0.draw()
        fix1.draw()
        fix2.draw()
        winSub.flip()
        if screenCount==2:
            msg.setText('t = %.3f' %timeNow)
            msg.draw()
            msgScanLength.draw()
            msgScanTr.draw()
            winOp.flip()
        #row+=1
        #core.wait(3.0/60.0)

        #count number of keypresses since previous frame, break if non-zero
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in responseKeys and respTimeCheck<respDuration:
                subjectResponse[numCoins]=1

        loopCounter +=1
        #core.wait(5.0)
        #outFile = open("debug.txt","w")
        #outFile.write(str(debugVar))
        #outFile.close()
        #numpy.savetxt('debug.txt',debugVar,fmt='%.3f')
        #numpy.savetxt('debugchop.txt',debugVar[:row,],fmt='%.3f')

    #calculate %age of responses that were correct
    #find non-nan
    #np.isnan(a) gives boolean array of true/a=false
    #np.isnan(a).any(1) gives a col vector of the rows with nans
    #~np.isnan(a).any(1) inverts the logic
    #myarray[~np.isnan(a).any(1)] gives the subset that I want
    findResp=subjectResponse[~numpy.isnan(subjectResponse)]
    calcResp=findResp[findResp==1]
    numCorrect=float(calcResp.shape[0])
    #print numCoins
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
    outFile='wedgeResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    if screenCount==2:
        winOp.close()
    winSub.close()
