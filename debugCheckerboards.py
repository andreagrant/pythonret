# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 14:34:12 2012

@author: agrant
"""
from psychopy import gui
from psychopy import core
from psychopy import visual
from psychopy import data
from psychopy import misc
from psychopy import event
from psychopy.visual import filters
import time, numpy, random
#import retinotopyScans
import matplotlib.pyplot as plot
import math
from array import *
#do full field flickering checkerboard
#length of scan in s
myDlg = gui.Dlg(title = "Retinotopy parameters")
myDlg.addField('Tr (s)',2)
myDlg.addField('# of cycles:',4)
myDlg.addField('Period (s)',10)
#myDlg.addField('pre scan duration (s)',12)
#myDlg.addField('Contrast (0 to 1)',0.5)
#myDlg.addField('# of scans',10)
myDlg.addField('pre scan duration (s)',0)
myDlg.addField('Contrast (0 to 1)',1)
myDlg.addField('# of scans',1)
myDlg.addField('Stimulus on external monitor?','Y')
#myDlg.addField('Monitor calibration file:',choices=['debug','3T','7T/PS','7T/AS','other'])
myDlg.addField('Monitor calibration file:',choices=['7T/AS','3T','7T/PS','debug','other'])
myDlg.show()#show dialog and wait for OK or Cancel
if myDlg.OK:#then the user pressed OK
    scanInfo = myDlg.data
    #print scanInfo
    #misc.toFile('retparams.pickle',scanInfo)
else:
    print('user cancelled')
    core.quit()
#
monCal='ASrearProj'
winSub = visual.Window([1024,768],monitor=monCal,units="deg",screen=1,
                               color=[-1.0,-1.0,-1.0],colorSpace='rgb',fullscr=True,allowGUI=False)
IR = 0.5
OR=12.0

scanLength=float(scanInfo[1]*scanInfo[2]+scanInfo[3])
#needs to be flexible--how do I extract the dims from screen?
#    screenSize=numpy.array([1600,1200])
screenSize=numpy.array([1024,768])
fixPercentage = 0.3
fixDuration=0.2
respDuration=1.0
subjectResponse=numpy.empty((scanLength*60/100,1))
subjectResponse[:]=numpy.nan
white=[1.0,1.0,1.0]
gray=[0.0,0.0,0.0]
black=[-1.0,-1.0,-1.0]
colorA=[1,0,0]#red in normal people's 0-1 world
colorB=[0,0.5,0]#black in normal people's 0-1 world

#convert colors to psychopy's scheme
colorAf=numpy.asarray(colorA,dtype=float)
colorBf=numpy.asarray(colorB,dtype=float)
colorAp=2*colorAf-1
colorBp=2*colorBf-1


#    image1=visual.SimpleImageStim(winSub,image='redblack1.jpg')
#    image2=visual.SimpleImageStim(winSub,image='redblack2.jpg')

#image1=visual.PatchStim(winSub,tex='redblack1a.jpg',mask=None,size=[OR,OR])

#let's try making some numpy arrays of the checkerboards! translated from matlab arrays
#size of image--hardcode for now, but needs to be 2^n that fits inside smaller screen dimension
imageSize=1024
halfSize=numpy.int(imageSize/2)
#create arrays of x,y, and r,theta
xIn=numpy.arange(-halfSize,halfSize,1)
yIn=numpy.arange(-halfSize,halfSize,1)
xIn.astype(float)
yIn.astype(float)
x,y=numpy.meshgrid(xIn,yIn)
r=numpy.sqrt(x**2+y**2)
xOverY=x/y
theta = numpy.arctan(xOverY)
theta[halfSize+1,halfSize+1]=0

#number of wedges (pairs!!)--eventually to be a var passed in
nWedges=8.0
#number of ring pairs
nRings=15.0
#width of wedges in radians
wedgeWidth = 2.0*math.pi/nWedges
ringWidth = 2.0/nRings
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
checkerBoardB[:,:,0]=checkerBoardBR
checkerBoardB[:,:,1]=checkerBoardBG
checkerBoardB[:,:,2]=checkerBoardBB

#finally, create the image textures!!
#oooh, these are fun--tiles the checkerboards!
#stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize)
#stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize)
stimA=visual.GratingStim(winSub,tex=checkerBoardA,size=imageSize,sf=1/imageSize,units='pix')
stimB=visual.GratingStim(winSub,tex=checkerBoardB,size=imageSize,sf=1/imageSize,units='pix')


ReverseFreq =8.0 #drift in Hz. could be an input param eventually?


#make a fixation cross which will rotate 45 deg on occasion
fix0 = visual.Circle(winSub,radius=IR/2.0,edges=32,lineColor=gray,lineColorSpace='rgb',
        fillColor=gray,fillColorSpace='rgb',autoLog=False)
fix1 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((0.0,-0.15),(0.0,0.15)),lineWidth=3.0,
        lineColor=black,lineColorSpace='rgb',
        fillColor=black,fillColorSpace='rgb',autoLog=False)

fix2 = visual.ShapeStim(winSub, pos=[0.0,0.0],vertices=((-0.15,0.0),(0.15,0.0)),lineWidth=3.0,
        lineColor=black,lineColorSpace='rgb',
        fillColor=black,fillColorSpace='rgb',autoLog=False)

#stim.setOri(t*rotationRate*360.0)
#stim.setRadialPhase(driftRate,'+')
#stim.setPos()#something here

msg1=visual.TextStim(winSub,pos=[0,+3],text='Hit a key when ready.')
msg1.draw()
winSub.flip()

#wait for subject
thisKey=None
while thisKey==None:
    thisKey = event.waitKeys(keyList=['r','g','b','y','q','escape'])
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

#draw the fixation point
#    wedge1.draw()
fix0.draw()
fix1.draw()
fix2.draw()
winSub.flip()
# and drift it
timeNow = scanTimer.getTime()
#row=1
msg = visual.TextStim(winSub, pos=[-screenSize[0]/2+45,-screenSize[1]/2+15],units='pix',text = 't = %.3f' %timeNow)
msg.draw()
loopCounter=0
fixTimer=core.Clock()
respTimer=core.Clock()
flickerTimer=core.Clock()

fixOri=0
numCoins=0
event.clearEvents()
#loop for the pre-scan rest duration time
while timeNow<scanInfo[3]:
    timeNow = scanTimer.getTime()
    #draw fixation
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
    fix0.draw()
    fix1.draw()
    fix2.draw()
    msg.setText('t = %.3f' %timeNow)
    msg.draw()
    winSub.flip()

#prepare for looping through the cycles
epochTimer = core.Clock()

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

    # alternate between stimulus and rest, starting with pre-scan duration of rest
    epochTime=epochTimer.getTime()
    #12s epoch of stimulus
    if epochTime<scanInfo[2]/2.0:
        chPhase=epochTime*2
        stimA.setPhase(chPhase)
        stimA.draw()
#        #alternate wedge 1&2 at flicker rate
#        flickerTimeCheck = flickerTimer.getTime()
#        if flickerTimeCheck<1/(2.0*ReverseFreq):
#            #first half of a period, show wedge 1
#            stimA.draw()
#            image1.draw()
#        elif flickerTimeCheck<1/ReverseFreq:
#            #second half of period, show wedge 2
#            stimB.draw()
#            image2.draw()
#        else:
#            #clocked over, reset timer
#            #could also do some modulus of timing
#            flickerTimer.reset()
        fix0.draw()
        fix1.draw()
        fix2.draw()
    elif epochTime<scanInfo[2]:
        #12s epoch of rest
        fix0.draw()
        fix1.draw()
        fix2.draw()
    else:
        epochTimer.reset()

    msg.setText('t = %.3f' %timeNow)
    msg.draw()
    winSub.flip()
    #row+=1
    #core.wait(3.0/60.0)

    #count number of keypresses since previous frame, break if non-zero
    for key in event.getKeys():
        if key in ['q','escape']:
            core.quit()
        elif key in ['r','g','b','y'] and respTimeCheck<respDuration:
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
percentCorrect=float(numCorrect)/(float(numCoins))

msgText='You got %f correct!' %(percentCorrect,)
msg1=visual.TextStim(winSub,pos=[0,+3],text=msgText)
msg1.draw()
winSub.flip()

numpy.savetxt('subresp.txt',subjectResponse)
core.wait(2)
