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

##########################################################################
##########################################################################
################################### VWFA localizer ############################
#################################### using imaages ###########################
##########################################################################

def VWFAlocImages(scanDict,screenSize=[1024,768]):
    #objects from
    #http://stims.cnbc.cmu.edu/Image%20Databases/TarrLab/Objects/
    #faces from
    #http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html
#
#more faces
#http://tarrlab.cnbc.cmu.edu/newsite/index.php?option=com_content&view=article&id=51&Itemid=61
#more objects
#http://stims.cnbc.cmu.edu/Image%20Databases/BOSS/

    #scenes
    #http://pirsquared.org/research/vhatdb/full/
    #houses
    #http://groups.csail.mit.edu/vision/SUN/

#    USING IN THE END:
    #houses
    #http://groups.csail.mit.edu/vision/SUN/
    #objects & chairs  from
    #http://stims.cnbc.cmu.edu/Image%20Databases/TarrLab/Objects/
    #faces from
    #http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html
     #more chairs from
     #????
    white=[1.0,1.0,1.0]
    gray=[0.0,0.0,0.0]
    black=[-1.0,-1.0,-1.0]

    fixPercentage =scanDict['fixFraction']
    fixDuration=0.25
    respDuration=1.0
    IR=scanDict['innerRadius']
    screenSize=scanDict['screenSize']

    #create a designmatrix
    #there are 4 categories of things to show
    #faces, places (houses), chairs (objects), and letters (words?)
    #also need rest in there
    #so need 4 columns in design matrix

    numTrials=210
    numImages=40*4
    designMatrix=numpy.zeros((numTrials,4))
    designMatrixX=numpy.zeros((numTrials,1))

    #first N Trs are already zero--rest
    #figure out when each stim should be on
    #for now, just get the frame working
    #hard code this as restABCDrestBADCrestCBDArestDCABrest
    #rests are 10s of gray, blocks are 10s of images
    #within each block, show 10 examples drawn randomly from a big list
    stimDur=0.75
    ISIdur=0.25
    trialLength=stimDur+ISIdur
    trialsPerBlock=10
    blockLength=trialLength*trialsPerBlock
    IBIdur=10
    #A: 10-20,70-80,140-150,180-190
    designMatrix[10:20,0]=1
    designMatrix[70:80,0]=1
    designMatrix[140:150,0]=1
    designMatrix[180:190,0]=1
    #B: 20-30,60-70,120-130,190-200
    designMatrix[20:30,1]=1
    designMatrix[60:70,1]=1
    designMatrix[120:130,1]=1
    designMatrix[190:200,1]=1

    #C: 30-40,90-100,110-120,170-180
    designMatrix[30:40,2]=1
    designMatrix[90:100,2]=1
    designMatrix[110:120,2]=1
    designMatrix[170:180,2]=1

    #D: 40-50,80-90, 130-140, 160-170
    designMatrix[40:50,3]=1
    designMatrix[80:90,3]=1
    designMatrix[130:140,3]=1
    designMatrix[160:170,3]=1

    #UGH i need to hack a new design matrix for the images without the rest spots in it
    designMatrixX[10:20,0]=1
    designMatrixX[70:80,0]=1
    designMatrixX[140:150,0]=1
    designMatrixX[180:190,0]=1
    #B: 20-30,60-70,120-130,190-200
    designMatrixX[20:30,0]=1
    designMatrixX[60:70,0]=1
    designMatrixX[120:130,0]=1
    designMatrixX[190:200,0]=1

    #C: 30-40,90-100,110-120,170-180
    designMatrixX[30:40,0]=1
    designMatrixX[90:100,0]=1
    designMatrixX[110:120,0]=1
    designMatrixX[170:180,0]=1

    #D: 40-50,80-90, 130-140, 160-170
    designMatrixX[40:50,0]=1
    designMatrixX[80:90,0]=1
    designMatrixX[130:140,0]=1
    designMatrixX[160:170,0]=1


    #length of scan in s
    scanLength=numTrials*trialLength
    # msgScanLength=visual.TextStim(winOp,pos=[0,2],text='Scan length (s): %.1f' %scanLength)
    # msgScanTr=visual.TextStim(winOp,pos=[0,1],text='No. of Volumes (at Tr=%.2f): %.0f' %(scanDict['Tr'],scanLength/scanDict['Tr']) )
    # msgScanLength.draw()
    # msgScanTr.draw()
    # winOp.flip()
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
    winSub = visual.Window(screenSize,monitor=scanDict['monCalFile'],units="deg",screen=scanDict['subjectScreen'],
                       color=gray,colorSpace='rgb',fullscr=False,allowGUI=False)
    subjectResponse=numpy.zeros((numTrials+1,1))
    subRespArray=numpy.zeros((numTrials+1,3))
    subjectResponse[:]=numpy.nan


   #prep display objects
    #get the list of files for each
    myPath=os.path.dirname(os.path.realpath(__file__))
    Aimages=glob.glob(os.path.join(myPath,'vwfaProcImages','faces256','*.png'))
    if len(Aimages)==0:
        Aimages=glob.glob(os.path.join(myPath,'vwfaProcImages','faces256','*.PNG'))
    if len(Aimages)==0:
        print('No face images found')
        core.quit()
    Bimages=glob.glob(os.path.join(myPath,'vwfaProcImages','houses256','*.jpg'))
    if len(Bimages)==0:
        Bimages=glob.glob(os.path.join(myPath,'vwfaProcImages','houses256','*.JPG'))
    if len(Bimages)==0:
        print('No house images found')
        core.quit()
    Cimages=glob.glob(os.path.join(myPath,'vwfaProcImages','chairs256','*.png'))
    if len(Cimages)==0:
        Cimages=glob.glob(os.path.join(myPath,'vwfaProcImages','chairs256','*.PNG'))
    if len(Cimages)==0:
        print('No chair images found')
        core.quit()
    Dimages=glob.glob(os.path.join(myPath,'vwfaProcImages','letters256','*.png'))
    if len(Dimages)==0:
        Dimages=glob.glob(os.path.join(myPath,'vwfaProcImages','letters256','*.PNG'))
    if len(Dimages)==0:
        print('No letter images found')
        core.quit()
    #print Aimages
    #print Bimages
    ##print Cimages
    #print Dimages
    numInList=numpy.zeros((4,1))
    numInList[0]=len(Aimages)
    numInList[1]=len(Bimages)
    numInList[2]=len(Cimages)
    numInList[3]=len(Dimages)
    #print numInList
    #generate my random sequence --need 40 of each list
    Asequence=numpy.random.randint(0,high=numInList[0],size=40)
    Bsequence=numpy.random.randint(0,high=numInList[1],size=40)
    Csequence=numpy.random.randint(0,high=numInList[2],size=40)
    Dsequence=numpy.random.randint(0,high=numInList[3],size=40)
    #now make one big list with all the filenames--much easier for showing them in the loop!!
    imageNameSequence = ['']*numImages
    Acounter=0
    Bcounter=0
    Ccounter=0
    Dcounter=0
    imCounter=0
    #for iIm in xrange(numTrials):?
    for iIm in range(numTrials):
        if designMatrix[iIm,0]==1:
            #next Aimage
            imageNameSequence[imCounter]=Aimages[Asequence[Acounter]]
            Acounter+=1
            imCounter+=1
        elif designMatrix[iIm,1]==1:
            #next Bimage
            imageNameSequence[imCounter]=Bimages[Bsequence[Bcounter]]
            Bcounter+=1
            imCounter+=1
        elif designMatrix[iIm,2]==1:
            #next Cimage
            imageNameSequence[imCounter]=Cimages[Csequence[Ccounter]]
            Ccounter+=1
            imCounter+=1
        elif designMatrix[iIm,3]==1:
            #next Dimage
            imageNameSequence[imCounter]=Dimages[Dsequence[Dcounter]]
            Dcounter+=1
            imCounter+=1
    numpy.savetxt('vwfaImagesdesignMatrix.txt',designMatrix,fmt='%.3i',header='faces,houses,chairs,letters')


    #make a fixation square which will enlarge on occasion
    fixSize=IR/2.0
    fix0 = visual.Rect(winSub,width=fixSize,height=fixSize,autoLog=False)
    fix0.setFillColor(color=[0.5,0.5,0.5],colorSpace='rgb')
    fix0.setLineColor(color=[1,-1,-1],colorSpace='rgb')

    #create the dictionary of images, but load only one
    currentImageNumber = 0
    imageStimDict=dict.fromkeys(numpy.arange(0,40*4))
#    imageStimDict[currentImageNumber]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber])
    imageStimDict[currentImageNumber]=visual.SimpleImageStim(winSub,image=imageNameSequence[currentImageNumber])

    msg1x=visual.TextStim(winSub, pos=[0,+8],text='visual wordform area localizer with images')
    msg1a = visual.TextStim(winSub, pos=[0,+5],text='During the scan, please keep your eyes on the + in the center.',height=1)
    msg1b = visual.TextStim(winSub, pos=[0,+2],text='Hit any button any time the fixation square becomes bigger.',height=1)
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
    #msg1c.draw()
    msg1a.draw()
    msg1b.draw()
    fix0.draw()
    #fix1.draw()
    #fix2.draw()
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
    timeNow=scanTimer.getTime()
    # msg = visual.TextStim(winOp,pos=[0,-1],text = 't = %.3f' %timeNow)
    # msg.draw()
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
    currentImageNumber = -1
    #loop through the number of trials, presenting appropriate stimulus or rest
    for iTrial in range(numTrials):
        #print iTrial
#        print designMatrix[iTrial,:]
        respTimer.reset()
        flipCoin=numpy.random.ranf()
        if flipCoin<fixPercentage:
            #change fixation size
            fixSize*=1.2
            fixTimer.reset()
            respTimer.reset()
            numCoins+=1
            subjectResponse[numCoins]=0
        fix0.setWidth(fixSize)
        fix0.setHeight(fixSize)

        if designMatrixX[iTrial,0]==1:
            #stim
            #load next image
            currentImageNumber+=1
            if currentImageNumber+1<len(imageNameSequence): #don't load an image past the last one!
                imageStimDict[currentImageNumber+1]=visual.ImageStim(winSub,image=imageNameSequence[currentImageNumber+1])

            #delete the 2nd previous one
            if currentImageNumber>3:
                del imageStimDict[currentImageNumber-1]
            #print imageStimDict[currentImageNumber]
            #print imageStimDict[currentImageNumber+1]
            #thisThing.draw()
            imageStimDict[currentImageNumber].draw()
            drawFix=0
            drawStim=1
            winSub.flip()
        else:
            #rest
            drawFix=1
            drawStim=0
            fix0.draw()
            #fix1.draw()
            #fix2.draw()

        #dispay stim for stimDuration amount of time
        trialTimerNew.add(stimDur)
        while trialTimerNew.getTime()>0:
            timeNow = scanTimer.getTime()
            fixTimeCheck=fixTimer.getTime()
            respTimeCheck=respTimer.getTime()
            #print trialTimerNew.getTime()
            if fixTimeCheck>fixDuration:
                fixSize=IR/2.0
                fix0.setWidth(fixSize)
                fix0.setHeight(fixSize)

            if drawStim==1:

                imageStimDict[currentImageNumber].draw()
            if drawFix==1:
                fix0.draw()

            # msg.setText('t = %.3f' %timeNow)
            # msg.draw()
            # msgScanLength.draw()
            # msgScanTr.draw()
            winSub.flip()
            # winOp.flip()
            for key in event.getKeys():
                if key in ['q','escape']:
                    core.quit()
                elif key in responseKeys and respTimeCheck<respDuration:
                    subjectResponse[numCoins]=1

        #then show fixation for ISI time
        trialTimerNew.add(trialLength-stimDur)
        while trialTimerNew.getTime()>0:
            #then show fixation for ISI time
            timeNow = scanTimer.getTime()
            fixTimeCheck=fixTimer.getTime()
            respTimeCheck=respTimer.getTime()
            #print trialTimerNew.getTime()
            if fixTimeCheck>fixDuration:
                fixSize=IR/2.0
                fix0.setWidth(fixSize)
                fix0.setHeight(fixSize)

            fix0.draw()
            winSub.flip()
            # msg.setText('t = %.3f' %timeNow)
            # msg.draw()
            # msgScanLength.draw()
            # msgScanTr.draw()
            # winOp.flip()
            for key in event.getKeys():
                if key in ['q','escape']:
                    core.quit()
                elif key in responseKeys and respTimeCheck<respDuration:
                    subjectResponse[numCoins]=1
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
    outFile='vwfaImResponse%04d%02d%02d_%02d%02d.txt'%(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    outFilePath=os.path.join('subjectResponseFiles',outFile)
    numpy.savetxt(outFilePath,findResp,fmt='%.0f')
    core.wait(2)
    # winOp.close()
    winSub.close()
