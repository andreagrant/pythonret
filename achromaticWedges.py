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
################### achromatic wedges  ###################################
################### asymmetric timing #######################################
#############################################################################

def achromaticWedges(scanDict, screenSize=[1024,768]):

    #do wedge
    #length of scan in s
    scanLength=float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
    #open subject window
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'], 
                       color=[0.0,0.0,0.0],colorSpace='rgb',fullscr=False,allowGUI=False)
    winOp = visual.Window([500,200],monitor='testMonitor',units='deg',screen=scanDict['operatorScreen'],
                          color=[0.0,0.0,0.0],colorSpace='rgb')

    msgScanLength=visual.TextStim(winOp,pos=[0,2],text='Scan length (s): %.1f' %scanLength)
    msgScanTr=visual.TextStim(winOp,pos=[0,1],text='No. of Volumes (at Tr=%.2f): %.0f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
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
    fixDuration=0.2
    respDuration=1.0
    subjectResponse=numpy.zeros((numpy.ceil(scanLength*60/100),1))
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
         size=OR*2,color=1,visibleWedge=wedgeSize,ori=0,interpolate=False,
         autoLog=False)

    altWedges=numpy.random.rand(10)
    for iGrr in xrange(0,10):
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

    driftFreq =2.0 #drift in Hz. could be an input param eventually? 

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
            
    msg1=visual.TextStim(winSub,pos=[0,+2],text='%s \n\nSubject: press a button when ready.'%scanNameText)
    msg1.draw()
    winSub.flip()
    
    #wait for subject
    thisKey=None
    while thisKey==None:
        thisKey = event.waitKeys(keyList=['r','g','b','y','1','2','3','4','q','escape'])
    if thisKey in ['q','escape']:
        core.quit() #abort
    else:
        event.clearEvents()        
#    while len(event.getKeys())==0: 
#        core.wait(0.05)
#    event.clearEvents()
    msg1=visual.TextStim(winSub,pos=[0,+3],text='Noise coming....')
    msg1.draw()
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
    epochTimer = core.Clock()
    #draw the stimulus
    for iWedge in xrange(0,20,2):
        wedge1.setOri(startOris[iWedge])
        wedge1.setRadialPhase(startPhases[iWedge/2])
        wedge1.draw()
        wedge1.setOri(startOris[iWedge+1])
        wedge1.setRadialPhase(startPhases[iWedge/2]+0.5)
        wedge1.draw()
    if offTimeBehavior==3:
        nowMask=maskA
        maskA.draw()
    fix0.draw()
    fix1.draw()
    fix2.draw()
    winSub.flip()
    nowPhase=startPhases
    # and drift it
    timeNow = scanTimer.getTime()
    #row=1
#    #msg = visual.TextStim(winSub, pos=[-screenSize[0]/2+45,-screenSize[1]/2+15],units='pix',text = 't = %.3f' %timeNow)
    msg = visual.TextStim(winOp,pos=[0,-1],text = 't = %.3f' %timeNow)
    msg.draw()
    loopCounter=0
    fixTimer=core.Clock() 
    respTimer=core.Clock()
    fixOri=0
    numCoins=0
    event.clearEvents()
    while timeNow<startTime+scanLength: #loop for scan duration
        timeBefore = timeNow    
        timeNow = scanTimer.getTime()
        deltaT=timeNow - startTime
        deltaTinc=timeNow-timeBefore
        
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
        epochTime=epochTimer.getTime()
        #display for period/2 time
        if epochTime<scanDict['period']/2.0:
            #lastPhase=nowPhase.copy()
            deltaPhase=driftFreq*deltaT
            #NowPhase=lastpHase+deltaPhase
            #set direction of drift--alternate every cycle
            setSign=math.floor(driftReverseFreq*deltaT)
            if setSign%2==0:
                phaseSign = 1.0
            else:
                phaseSign = -1.0
            phaseSignVec=phaseSign*altWedges
            nowPhase=startPhases + deltaPhase*(phaseSignVec)
            for iWedge in xrange(0,20,2):
                wedge1.setOri(startOris[iWedge])
                wedge1.setRadialPhase(nowPhase[iWedge/2])
                wedge1.draw()
                wedge1.setOri(startOris[iWedge+1])
                wedge1.setRadialPhase(nowPhase[iWedge/2]+0.5*phaseSignVec[iWedge/2])
                wedge1.draw()

            if offTimeBehavior==3:
                nowMask.draw()
            fix0.draw()
            fix1.draw()
            fix2.draw()
        elif epochTime<scanDict['period']:
            #draw either no checkerboard or static checkerboard, depending on scan
            if offTimeBehavior==1:
                #turn it OFF
                #just draw fixation
                fix0.draw()
                fix1.draw()
                fix2.draw()
            elif offTimeBehavior==2:
                #draw static
                for iWedge in xrange(0,20,2):
                    wedge1.setOri(startOris[iWedge])
                    wedge1.setRadialPhase(nowPhase[iWedge/2])
                    wedge1.draw()
                    wedge1.setOri(startOris[iWedge+1])
                    wedge1.setRadialPhase(nowPhase[iWedge/2]+0.5*phaseSignVec[iWedge/2])
                    wedge1.draw()

                fix0.draw()
                fix1.draw()
                fix2.draw()
            elif offTimeBehavior==3:
                #keep drifting, change mask
                nowMask=maskB
                #lastPhase=nowPhase.copy()
                deltaPhase=driftFreq*deltaT
                #set direction of drift--alternate every cycle
                setSign=math.floor(driftReverseFreq*deltaT)
                if setSign%2==0:
                    phaseSign = 1.0
                else:
                    phaseSign = -1.0
                phaseSignVec=phaseSign*altWedges
                nowPhase=startPhases + deltaPhase*(phaseSignVec)
                for iWedge in xrange(0,20,2):
                    wedge1.setOri(startOris[iWedge])
                    wedge1.setRadialPhase(nowPhase[iWedge/2])
                    wedge1.draw()
                    wedge1.setOri(startOris[iWedge+1])
                    wedge1.setRadialPhase(nowPhase[iWedge/2]+0.5*phaseSignVec[iWedge/2])
                    wedge1.draw()
                nowMask.draw()
                fix0.draw()
                fix1.draw()
                fix2.draw()
        else:
            #reset the epoch timer
            epochTimer.reset()
            #if using a mask, set back to first one
            if offTimeBehavior==3:
                nowMask=maskA

        msg.setText('t = %.3f' %timeNow)
        msg.draw()
        msgScanLength.draw()
        msgScanTr.draw()
        winSub.flip()
        winOp.flip()
        #row+=1
        #core.wait(3.0/60.0)
    
        #count number of keypresses since previous frame, break if non-zero
        for key in event.getKeys():
            if key in ['q','escape']:
                core.quit()
            elif key in ['r','g','b','y','1','2','3','4'] and respTimeCheck<respDuration:
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
    outFile='achromResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    winOp.close()
    winSub.close()



#    #full field(?) achromatic wedges
#    #length of scan in s
#    scanLength=float(scanDict['numCycles']*scanDict['period']+scanDict['preScanRest'])
#    #open subject window
#    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'], 
#                       color=[-1.0,-1.0,-1.0],colorSpace='rgb',fullscr=True,allowGUI=False)
#    #needs to be flexible--how do I extract the dims from screen?
##    screenSize=numpy.array([1600,1200])
#    #screenSize=numpy.array([1024,768])
#    #parse out vars from scanDict
#    IR=scanDict['innerRadius']
#    OR=scanDict['outerRadius']
#    colorBG=scanDict['colorBackground']
#    flickFreq=scanDict['animFreq']
#    timeBase=scanDict['timeBase']
#    fixPercentage =scanDict['fixFraction']
#    fixDuration=0.25
#    respDuration=1.0
#    subjectResponse=numpy.zeros((scanLength*60/100,1))
#    subRespArray=numpy.zeros((scanLength*60/100,3))
#    subjectResponse[:]=numpy.nan
#    #plotResp=numpy.zeros((2,2))
##    plotRespWrong=numpy.zeros((2,2))
#    plotMax=scanLength*60/100
#    plotResp=numpy.zeros((plotMax,2))
#    plotColors=numpy.zeros((plotMax,3))
#    #axesX=numpy.arange(0,scanLength*60/100)
#    white=[1.0,1.0,1.0]
#    gray=[0.0,0.0,0.0]
#    black=[-1.0,-1.0,-1.0]
#    
##    plt.ion()
##    plt.plot(plotResp[0:2],'ro')
##    plt.ylabel('subject responses')
##    plt.show()
##    plt.axis([0,scanLength*0.6,-0.1,1.1])    
#    
#    operatorWindow=visual.Window([1024,768],monitor='testMonitor',units='deg',screen=scanDict['operatorScreen'],color=[0,0,0],colorSpace='rgb')                       
#    
#    opPlot=visual.ElementArrayStim(operatorWindow,units='pix',xys=plotResp,sizes=7,nElements=plotMax,fieldPos=(-500,-384),
#                                   colors=plotColors,colorSpace='rgb',sfs=0,fieldShape='square',
#                                   elementMask='circle')
#    gridLinesVertices=numpy.zeros((46,2))
#    gridLinesVertices[:,0]=[0,998,0,0,998,0,0,998,0,0,998,0,0,998,0,0,998,100,100,100,200,200,200,300,300,300,400,400,400,500,500,500,600,600,600,700,700,700,800,800,800,900,900,900,998,998]
#    gridLinesVertices[:,1]=[0,0,0,100,100,100,200,200,200,300,300,300,400,400,400,500,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0,500,500,0]
#    opPlotGrid=visual.ShapeStim(operatorWindow,units='pix',vertices=gridLinesVertices,closeShape=False,pos=(-512,-334))
#    #labels for the plot regions
#    plotLabel1=visual.TextStim(operatorWindow,units='pix',pos=(-450,150),alignHoriz='left',text='Correct (active--displayed \'X\' and got a button press)',color=(-1,1,-1),colorSpace='rgb',height=15)
#    plotLabel2=visual.TextStim(operatorWindow,units='pix',pos=(-450,-250),alignHoriz='left',text='Wrong (\'X\' displayed, NO button press)',color=(1,-1,-1),colorSpace='rgb',height=15)
#    plotLabel3=visual.TextStim(operatorWindow,units='pix',pos=(-450,-150),alignHoriz='left',text='Wrong-ish (No \'X\', but got a button press!?)',color=(1,-1,-1),colorSpace='rgb',height=15)
#    plotLabel4=visual.TextStim(operatorWindow,units='pix',pos=(-450,25),alignHoriz='left',text='Correct (passive--no \'X\', no button press)',color=(-1,-1,1),colorSpace='rgb',height=15)
#    #create a designmatrix for trigger-based counting
#    #first create an array--length = total number of Trs
#    numTr=scanLength/scanDict['Tr']
#    designMatrix=numpy.zeros((numTr,1))    
#
#    #first N Trs are already zero--rest
#    #figure out when the stim should be on
#    for iStim in range(scanDict['numCycles']):
#        restAmt=scanDict['preScanRest']/scanDict['Tr']
#        stimDur=scanDict['period']/scanDict['Tr']
#        firstVal=restAmt + iStim*stimDur
#        lastVal=firstVal + scanDict['period']/(2*scanDict['Tr'])
#        designMatrix[firstVal:lastVal]=1
#    numpy.savetxt('debug.txt',designMatrix,fmt='%.3i')
#
#    #convert colors to psychopy's scheme
#    colorBGf=numpy.asarray(colorBG,dtype=float)
#    colorBGp=2*colorBGf-1
#
# 
#    #let's try making some numpy arrays of the checkerboards! translated from matlab arrays
#    #size of image--hardcode for now, but needs to be 2^n that fits inside smaller screen dimension
##    twoN=numpy.ones((13))    
##    for n in range(13):
##        twoN[n]=pow(2.0,n)
##    twoNsize=numpy.nonzero(twoN>screenSize[1])
##    #hmm, this somehow made a nested tuple, whatever that is
##    keep_n=twoNsize[0][0]-1
##    imageSize=pow(2,keep_n)
##    halfSize=numpy.int(imageSize/2)
#    debugVar=numpy.zeros((scanLength*60,2))
#    #imageSize=1024
#    if screenSize[0]<257:
#        imageSize=256
#    elif screenSize[0]<513:
#        imageSize=512
#    elif screenSize[0]<1025:
#        imageSize=1024
#    elif screenSize[0]<2057:
#        imageSize=2048
#    halfSize=numpy.int(imageSize/2)
#        
#    print type(imageSize)
#    print type(halfSize)
#    #create arrays of x,y, and r,theta
#    xIn=numpy.arange(-halfSize,halfSize,1)
#    yIn=numpy.arange(-halfSize,halfSize,1)
#    xIn.astype(float)
#    yIn.astype(float)
#    x,y=numpy.meshgrid(xIn,yIn)
#    r=numpy.sqrt(x**2+y**2)
#    #avoid divide by zero issues
#    y[y==0]=numpy.finfo(numpy.float).eps
#    xOverY=x/y
#    theta = numpy.arctan(xOverY)
#    theta[halfSize+1,halfSize+1]=0
#    
#    #number of wedges (NOT pairs!!)
#    nWedges=72.0
#    #number of rings 
#    nRings=3.0
#    #width of wedges in radians
#    wedgeWidth = 2.0*math.pi/nWedges #CHECK
#    ringWidth = 2.0/nRings#1/over? #CHECK
#    #ring function--describes how the ring width increases with eccentricity
#    ringFunction=numpy.power(r/halfSize,0.3)+0.2
#    
#    wedgeMask = 0.5 - (numpy.mod(theta,wedgeWidth)>(wedgeWidth/2.0)) 
#    rmA=numpy.mod(ringFunction,ringWidth)>(ringWidth/2.0)
#    ringMask = 1 - 2.0*(rmA)
#    
#    checkerBoardLogic=wedgeMask*ringMask + 0.5
#    #checkerBoardBG=r>
#    #initialize an array of 1024x1024x3 for RGB channels
#    checkerBoardA=numpy.ones((imageSize, imageSize,3))
#    checkerBoardAR=numpy.ones((imageSize, imageSize))
#    checkerBoardAB=numpy.ones((imageSize, imageSize))
#    checkerBoardAG=numpy.ones((imageSize, imageSize))
#    #set the RGB values based on the colors passed in during launch
#    #CBA, logic=1-->colorB, logic=0-->colorA
#    #CBB, logic=1-->colorA, logic=0-->colorB
#    #color A, column 1
#    checkerBoardAR[checkerBoardLogic==1] = colorAp[0]
#    checkerBoardAG[checkerBoardLogic==1] = colorAp[1]
#    checkerBoardAB[checkerBoardLogic==1] = colorAp[2]
#    checkerBoardAR[checkerBoardLogic==0] = colorBp[0]
#    checkerBoardAG[checkerBoardLogic==0] = colorBp[1]
#    checkerBoardAB[checkerBoardLogic==0] = colorBp[2]
#    #now add in the background color around the widest ring
##    imageMask=numpy.ones((imageSize,imageSize))
# #   imageMask[r>halfSize]=-1
#    checkerBoardAR[r>halfSize]=colorBGp[0]
#    checkerBoardAG[r>halfSize]=colorBGp[1]
#    checkerBoardAB[r>halfSize]=colorBGp[2]
#    #smoosh the arrays together
#    checkerBoardA[:,:,0]=checkerBoardAR
#    checkerBoardA[:,:,1]=checkerBoardAG
#    checkerBoardA[:,:,2]=checkerBoardAB
#    
#    checkerBoardB=numpy.ones((imageSize, imageSize,3))
#    checkerBoardBR=numpy.ones((imageSize, imageSize))
#    checkerBoardBB=numpy.ones((imageSize, imageSize))
#    checkerBoardBG=numpy.ones((imageSize, imageSize))
#    checkerBoardBR[checkerBoardLogic==1] = colorBp[0]
#    checkerBoardBG[checkerBoardLogic==1] = colorBp[1]
#    checkerBoardBB[checkerBoardLogic==1] = colorBp[2]
#    checkerBoardBR[checkerBoardLogic==0] = colorAp[0]
#    checkerBoardBG[checkerBoardLogic==0] = colorAp[1]
#    checkerBoardBB[checkerBoardLogic==0] = colorAp[2]
#    checkerBoardBR[r>halfSize]=colorBGp[0]
#    checkerBoardBG[r>halfSize]=colorBGp[1]
#    checkerBoardBB[r>halfSize]=colorBGp[2]
#    checkerBoardB[:,:,0]=checkerBoardBR
#    checkerBoardB[:,:,1]=checkerBoardBG
#    checkerBoardB[:,:,2]=checkerBoardBB
#    #finally, create the image textures!!
#    #oooh, these are fun--tiles the checkerboards!
#    #stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize)
#    #stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize)
#    stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize,sf=1/imageSize,units='pix',texRes=imageSize)
#    stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize,sf=1/imageSize,units='pix')
#
#   
#    ReverseFreq =flickFreq #drift in Hz. could be an input param eventually? 
#
#    
#    #make a fixation cross which will rotate 45 deg on occasion
#    fix0 = visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
#            fillColor=gray,fillColorSpace='rgb',autoLog=False)
#    fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.2),(0.0,0.2)),lineWidth=3.0,
#            lineColor=black,lineColorSpace='rgb',
#            fillColor=black,fillColorSpace='rgb',autoLog=False)
#    
#    fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.2,0.0),(0.2,0.0)),lineWidth=3.0,
#            lineColor=black,lineColorSpace='rgb',
#            fillColor=black,fillColorSpace='rgb',autoLog=False)
#    
#    #stim.setOri(t*rotationRate*360.0)
#    #stim.setRadialPhase(driftRate,'+')
#    #stim.setPos()#something here
#    msg1x=visual.TextStim(winSub, pos=[0,+8],text='flickering checkerboard, asymmetric timing')
#    msg1a = visual.TextStim(winSub, pos=[0,+5],text='During the scan, please keep your eyes on the + in the center.',height=1)    
#    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Hit any button any time the + becomes an X.',height=1)    
#    msg1=visual.TextStim(winSub,pos=[0,-3],text='Subject: Hit a key when ready.',color=[1,-1,-1],colorSpace='rgb')
#    msg1.draw()
#    msg1a.draw()
#    msg1b.draw()
#    msg1x.draw()
#    fix0.draw()
#    fix1.draw()
#    fix2.draw()
#    winSub.flip()
#
#
#    #wait for subject
#    thisKey=None
#    while thisKey==None:
#        thisKey = event.waitKeys(keyList=['r','g','b','y','q','escape'])
#    if thisKey in ['q','escape']:
#        core.quit() #abort
#    else:
#        event.clearEvents()        
##    while len(event.getKeys())==0: 
##        core.wait(0.05)
##    event.clearEvents()
##    msg1=visual.TextStim(winSub,pos=[0,+1],text='Waiting for magnet....',color=[1,1,1],colorSpace='rgb',height=3)
##    msg1.draw()
##    fix0.draw()
##    fix1.draw()
##    fix2.draw()
##    winSub.flip()
#    msg1a = visual.TextStim(winSub, pos=[0,+5],text='   ',height=1)    
#    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Waiting for magnet',height=1)    
#    #msg1c=visual.TextStim(winSub,pos=[0,-3],text='Subject: Hit a key when ready.',color=[1,-1,-1],colorSpace='rgb')
#    msg1c.draw()
#    msg1a.draw()
#    msg1b.draw()
#    fix0.draw()
#    fix1.draw()
#    fix2.draw()
#    winSub.flip()
#  
#    #wait for trigger
#    trig=None
#    while trig==None:
#        #wait for trigger "keypress"
#        trig=event.waitKeys(keyList=['t','5','q','escape'])
#    if trig in ['q','escape']:
#        core.quit()
#    else: #stray key
#        event.clearEvents()
#    
#    #start the timer            
#    scanTimer=core.Clock()
#    startTime=scanTimer.getTime()
#
#    #draw the fixation point
##    wedge1.draw()
#    fix0.draw()
#    fix1.draw()
#    fix2.draw()
#    winSub.flip()
#    # and drift it
#    timeNow = scanTimer.getTime()
#    #row=1
#    msg = visual.TextStim(operatorWindow,units='pix',pos=(0.0,325.0),text = 't = %.3f' %timeNow)
#    msg.draw()
#    loopCounter=0
#    restLoopCounter=0
#    TrCounter=0
#    if timeBase==0:
#        ttp=TrCounter+1
#        msgTr=visual.TextStim(operatorWindow,units='pix',pos=(0.0,275.0),text='Tr = %i' %ttp)
#        msgTr.draw()
#    msg4 = visual.TextStim(operatorWindow,units='pix',text = 'percent correct',pos=(0.0,-10),height=2)
#    msg4.draw()
#    msg5 = visual.TextStim(operatorWindow,units='pix',text = 'time since correct',pos=(0.0,-15),height=2)
#    msg5.draw()
#    
#
#    fixTimer=core.Clock() 
#    respTimer=core.Clock()
#    flickerTimer=core.Clock()
#
#    fixOri=0
#    numCoins=0
#    event.clearEvents()
#    for key in event.getKeys():
#        if key in ['q','escape']:
#            core.quit()
#        elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
#            subjectResponse[numCoins]=1
#    #time based loop advancement
#   
#    respCounter=0
#   
#    #display rest for pre-scan duration
#    while timeNow<scanDict['preScanRest']:
#        timeNow = scanTimer.getTime()
#        #draw fixation
#        #every 100 frames, decide if the fixation point should change or not
#        if restLoopCounter%100 ==0 and restLoopCounter>10:
#            #flip a coin to decide
#            flipCoin=numpy.random.ranf()
#            if flipCoin<fixPercentage: 
#                #reset timers/change ori
#                fixOri=45
#                fixTimer.reset()
#                respTimer.reset()
#                numCoins+=1
#                subjectResponse[numCoins]=0
#            #store info--expected response or not?
#            respCounter+=1
#            subRespArray[respCounter,0]=timeNow
#            subRespArray[respCounter,1]=flipCoin<fixPercentage
#        fixTimeCheck=fixTimer.getTime()
#        respTimeCheck=respTimer.getTime()
#        if fixTimeCheck >fixDuration: #timer expired--reset ori
#            fixOri=0
#
#        fix1.setOri(fixOri)
#        fix2.setOri(fixOri)
#        fix0.draw()
#        fix1.draw()
#        fix2.draw()
#        msg.setText('t = %.3f' %timeNow)
#        msg.draw()
#        winSub.flip()
#        operatorWindow.flip()
#        for key in event.getKeys():
#            if key in ['q','escape']:
#                core.quit()
#            elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
#                subjectResponse[numCoins]=1
#                plotResp[numCoins]=1
#                subRespArray[respCounter,2]=1
##                elif key in ['t']:
##                    #increment loop count for each trigger 
##                    restLoopCounter +=1
#        #update the operator graph
#        #determine response correctness and append to plot vertices variable
#        plotResp[respCounter,0]=respCounter
#        if subRespArray[respCounter,1]==1 and subRespArray[respCounter,2]==1:
#             #exp resp and got resp--correct and awake
#             plotResp[respCounter,1]=500
#             plotColors[respCounter,0]=-1
#             plotColors[respCounter,1]=1
#             plotColors[respCounter,2]=-1
##                 plotResp=numpy.append(plotResp,[[respCounter,500]],0)
#             #opPlotRight.setLineColor([-1,1,-1])
#        elif subRespArray[respCounter,1]==1 and subRespArray[respCounter,2]==0:
#            #exp response, got NONE--wrong!
#             plotResp[respCounter,1]=100
#             plotColors[respCounter,0]=1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=-1
##                 plotRespWrong=numpy.append(plotRespWrong,[[respCounter,200]],0)
#             #opPlotRight.setLineColor([1,-1,-1])
#        elif subRespArray[respCounter,1]==0 and subRespArray[respCounter,2]==1:
#             #exp NONE, got response--wrong, but awake at least
#             plotResp[respCounter,1]=150
#             plotColors[respCounter,0]=1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=-1
##                plotRespWrong=numpy.append(plotRespWrong,[[respCounter,250]],0)
#            #opPlotRight.setLineColor([1,-1,-1])
#        elif subRespArray[respCounter,1]==0 and subRespArray[respCounter,2]==0:
#            #exp none, got NONE--correct, but uninformative
#             plotResp[respCounter,1]=400
#             plotColors[respCounter,0]=-1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=1
##                plotResp=numpy.append(plotResp,[[respCounter,450]],0)
#            #opPlotRight.setLineColor([-1,1,-1])
#        #update the vertices
#        plotLabel1.draw()
#        plotLabel2.draw()
#        plotLabel3.draw()
#        plotLabel4.draw()
#        opPlotGrid.draw()
#        opPlot.setXYs(plotResp)
#        opPlot.setColors(plotColors)
#        opPlot.draw()
#        restLoopCounter+=1
##            if restLoopCounter%300 and restLoopCounter>5:
##                plt.plot(plotResp[0:numCoins+1],'ro')            
##                plt.draw
#
#    
#    #pre-scan rest is done.        
#    #prepare for looping through the cycles
#    epochTimer = core.Clock()
#
#
#    #time based looping through stimulus
#    while timeNow<startTime+scanLength: #loop until total scan duration has elapsed
#        timeBefore = timeNow    
#        timeNow = scanTimer.getTime()
#        deltaT=timeNow - startTime
#        deltaTinc=timeNow-timeBefore
#        
#        #every 100 frames, decide if the fixation point should change or not
#        if loopCounter%100 ==0 and loopCounter>10:
#            #flip a coin to decide
#            flipCoin=numpy.random.ranf()
#            if flipCoin<fixPercentage: 
#                #reset timers/change ori
#                fixOri=45
#                fixTimer.reset()
#                respTimer.reset()
#                numCoins+=1
#                subjectResponse[numCoins]=0
#                plotResp[numCoins]=1
#            #store info--expected response or not?
#            respCounter+=1
#            subRespArray[respCounter,0]=timeNow
#            subRespArray[respCounter,1]=flipCoin<fixPercentage
#        fixTimeCheck=fixTimer.getTime()
#        respTimeCheck=respTimer.getTime()
#        if fixTimeCheck >fixDuration: #timer expired--reset ori
#            fixOri=0
#
#        fix1.setOri(fixOri)
#        fix2.setOri(fixOri)
#        
#        # display stimulus for stimDuration time, then rest for restDuration time
#        epochTime=epochTimer.getTime()
#        # epoch of stimulus
#        if epochTime<scanDict['stimDuration']:
#            #alternate wedge 1&2 at flicker rate
#            flickerTimeCheck = flickerTimer.getTime()
#            if flickerTimeCheck<1/(2.0*ReverseFreq):
#                #first half of a period, show wedge 1
#                #image1.draw()
#                stimA.draw()
#            elif flickerTimeCheck<1/ReverseFreq:
#                #second half of period, show wedge 2
##                image2.draw()
#                 stimB.draw()               
#            else:
#                #clocked over, reset timer
#                #could also do some modulus of timing
#                flickerTimer.reset()
#            fix0.draw()
#            fix1.draw()
#            fix2.draw()
#        elif epochTime<scanDict['period']:
#            #rest for REMAINDER of full period (restDuration implicit)
#            fix0.draw()
#            fix1.draw()
#            fix2.draw()
#        else:
#            epochTimer.reset()
#        
#        msg.setText('t = %.3f' %timeNow)
#        msg.draw()
#        operatorWindow.flip()
#        winSub.flip()
#        #row+=1
#        #core.wait(3.0/60.0)
#    
#        #count number of keypresses since previous frame, break if non-zero
#        for key in event.getKeys():
#            if key in ['q','escape']:
#                core.quit()
#            elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
#                subjectResponse[numCoins]=1
#                subRespArray[respCounter,2]=1
##            if loopCounter%300 and loopCounter>5:
##                plt.plot(plotResp[0:numCoins+1],'ro')            
##                plt.draw
#
#        #update the operator graph
#        #determine response correctness and append to plot vertices variable
##            print respCounter
##            print subRespArray[respCounter,1]
##            print subRespArray[respCounter,2]
#        plotResp[respCounter,0]=respCounter
#        if subRespArray[respCounter,1]==1 and subRespArray[respCounter,2]==1:
#             #exp resp and got resp--correct and awake
#             plotResp[respCounter,1]=500
#             plotColors[respCounter,0]=-1
#             plotColors[respCounter,1]=1
#             plotColors[respCounter,2]=-1
##                 plotResp=numpy.append(plotResp,[[respCounter,500]],0)
#             #opPlotRight.setLineColor([-1,1,-1])
#        elif subRespArray[respCounter,1]==1 and subRespArray[respCounter,2]==0:
#            #exp response, got NONE--wrong!
#             plotResp[respCounter,1]=100
#             plotColors[respCounter,0]=1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=-1
##                 plotRespWrong=numpy.append(plotRespWrong,[[respCounter,200]],0)
#             #opPlotRight.setLineColor([1,-1,-1])
#        elif subRespArray[respCounter,1]==0 and subRespArray[respCounter,2]==1:
#             #exp NONE, got response--wrong, but awake at least
#             plotResp[respCounter,1]=150
#             plotColors[respCounter,0]=1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=-1
##                plotRespWrong=numpy.append(plotRespWrong,[[respCounter,250]],0)
#            #opPlotRight.setLineColor([1,-1,-1])
#        elif subRespArray[respCounter,1]==0 and subRespArray[respCounter,2]==0:
#            #exp none, got NONE--correct, but uninformative
#             plotResp[respCounter,1]=400
#             plotColors[respCounter,0]=-1
#             plotColors[respCounter,1]=-1
#             plotColors[respCounter,2]=1
##                plotResp=numpy.append(plotResp,[[respCounter,450]],0)
#            #opPlotRight.setLineColor([-1,1,-1])
#        #update the vertices
#        plotLabel1.draw()
#        plotLabel2.draw()
#        plotLabel3.draw()
#        plotLabel4.draw()
#        opPlotGrid.draw()
#        opPlot.setXYs(plotResp)
#        opPlot.setColors(plotColors)
#        opPlot.draw()
#        loopCounter +=1        
#        
#
#    findResp=subjectResponse[~numpy.isnan(subjectResponse)]
#    calcResp=findResp[findResp==1]
#    numCorrect=float(calcResp.shape[0])
#    percentCorrect=float(numCorrect)/(float(numCoins))
#    
#    msgText='You got %f correct!' %(percentCorrect,)
#    msg1=visual.TextStim(winSub,pos=[0,+3],text=msgText)
#    msg1.draw()
#    winSub.flip()
#
#    numpy.savetxt('subresp.txt',subjectResponse)
#    core.wait(2)
#    operatorWindow.close()
#    winSub.close()
#