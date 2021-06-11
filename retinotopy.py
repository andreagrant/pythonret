#import libraries
#import pyglet
#pyglet.options['shadow_window'] = False
from psychopy import visual
from psychopy import gui
from psychopy import core
from psychopy import data
from psychopy import misc
from psychopy import event
from psychopy.visual import filters
from psychopy import monitors
import time, numpy, random
#pyglet.options['shadow_window'] = False
#import retinotopyScans
import math
from array import *
import os
import glob
import imp

import datetime
import platform
#import psychopy.info
import unicodedata
from wedgeScan import wedgeScan
from ringScan2 import ringScan
from motionScan import motionScan
from objectScan import objectScan
from flickerScan2 import flickerScan
from flickerScanArb2 import flickerScanArb
from driftChecker import driftChecker
from driftCheckerArb import driftCheckerArb
from driftChecker3mask import driftChecker3mask
from achromaticWedges import achromaticWedges
from isolumCheckerScan import isolumCheckerScan
from VWFAloc import VWFAloc
from VWFAlocImages import VWFAlocImages
from flasher import flasher







##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
############################# main #######################################
##########################################################################
##########################    CODE   ####################################
##########################################################################
##########################################################################
##########################   STARTS    #####################################
##########################################################################
##########################################################################
############################  HERE   ######################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################

#get path
myPath=os.path.dirname(os.path.realpath(__file__))

##figure out subject's screen number
#iScreen=0
#while iScreen<10:
#    testWin=visual.Window([600,600],monitor='testMonitor',screen=iScreen)
#    textAsk=visual.TextStim(testWin,text='is this the subject\'s screen? (y/n)')
#    textAsk.draw()
#    testWin.flip()
#    thisKey=None
#    while thisKey==None:
#        thisKey=event.waitKeys(keyList=['y','Y','n','N'])
#    if thisKey[0] in ['y','Y']:
#        subScreen=iScreen
#        iScreen=11
#    else:
#        iScreen+=1
#    testWin.close()
#print subScreen
screenNums=[0,1]
p=platform.platform()
if 'Windows' in p:
    thisPlatform=1
elif 'Darwin' in p:
    thisPlatform=2
elif 'Linux' in p:
    thisPlatform=3
    #need to know this so we can force single screen for linux.
    #screenNums=[0,0]
else:
    thisPlatform=0
#pop up a menu to choose the running mode
# root=Tk()
# app=runModeButtonBox(root)
# root.mainloop()
# scanMode=numpy.int(app.v.get())
myDlg = gui.Dlg(title="Scanning mode: parameter file or menu-driven?")
myDlg.addText('By running this code, YOU AGREE to cite the')
myDlg.addText('relevant references (listed in the documentation)')
myDlg.addText('in any publications that use these stimuli')
myDlg.addText('If you DISAGREE, click cancel.')
myDlg.addField('Scanning mode:', choices=["dynamic menu-driven","parameter file"])
myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # then the user pressed OK
    thisInfo = myDlg.data
    #print thisInfo
    if "parameter" in thisInfo[0]:
        scanMode=1
    else:
        scanMode=2
else:
    print('user cancelled')

#if param file based, get the param file
if scanMode==1:
    #parameter file
    # root = Tk()
    # root.withdraw()
    print('before')
    thisFileU=gui.fileOpenDlg()
    files=str(thisFileU[0])

    print('after')
    if len(files)==0:
        #user cancelled--abort
        core.quit()
    else:
        #get the scan parameters from the file--should have 11 items
        imp.load_source('inVars',files)
        from inVars import scanDict
        from inVars import scanSeq
        numScans = scanDict['numScans']
        scanDict['platform']=thisPlatform
        #check for trigger/response and add defaults if not there
        if 'trigger' not in scanDict:
            scanDict['trigger']='t5'
        if 'subjectResponse' not in scanDict:
            scanDict['subjectResponse']='rgby1234'
elif scanMode==2:
    #otherwise, ask for scan timing specs and then scan sequence
    #get general scan parameters and number of scans
    #try to load scanDict from lastrun pickle file
    if os.path.isfile('lastrun.pickle')==True:
        #found a lastrun file--load scanDict from it
        scanDict=misc.fromFile('lastrun.pickle')
        #scanDict['animFreq']=2
        #scanDict['pairWedge']=1
        #check for trigger/response and add defaults if not there
        if 'trigger' not in scanDict:
            scanDict['trigger']='t5'
        if 'subjectResponse' not in scanDict:
            scanDict['subjectResponse']='rgby1234'

    else:
        #define defaults
        scanDict={
        #Tr (s)
        'Tr':2,
        #number of cycles (traveling wave cycle or stim-rest pairs)
        'numCycles':10,
        #period (s) of each cycle
        'period':24,
        #pre-scan duration (s) --rest before start OR traveling wave to show during throw-away time
        'preScanRest':12,
        #contrast for retinotopy, 0 to 1
        'contrast':1.0,
        #inner radius of stimulus (degrees)
        'innerRadius':0.5,
        #outer radius of stimulus (degrees)
        'outerRadius':12.0,
        #Monitor calibration filename
        #choices are: 7TASwest 7TASeast    3TA  3TB  7TPS   debug   other
        'monitor':'other',
        #screen number for operator (normally 0 unless Yedi gets confused)
        'operatorScreen':0,
        #screen number for subject (normally 1)
        'subjectScreen':1,
        #fraction of time the fixation point could change
        'fixFraction':0.2,
        #wedge width for wedges, degrees
        'wedgeWidth':45,
        #duty cycle for rings, %
        'dutyCycle':25,
        #animation (drift/flicker) frequency, Hz
        'animFreq':0.2,
        #whether (1) or not (0) to show a second wedge at 180
        'pairWedge':0,
        #color A of flickering checkerboard as RGB triplet (0 to 1)
        'colorA':'1,0,0',
        #color B of flickering checkerboard as RGB triplet (0 to 1)
        'colorB':'0,0,0',
        #background color for flickering checkerboard as RGB triplet (0 to 1)
        'colorBackground':'0.5,0.5,0.5',
        #stimulus duration for asymmetric timing
        'stimDuration':1,
        #whether time control is advance by clock time (1) or triggers (0)
        'timeBase':1,
        #radius for center/A/inner/B/outer checkerboards
        'Ralpha':1.0,
        #radius for center/A/inner/B/outer checkerboards
        'Rbeta':2.0,
        #fixation style: 1 for just rotation, 2 for rotation and color change
        'fixationStyle':1,
        #trigger key
        'trigger':'t5',
        #subject responses
        'subjectResponse':'rgby1234',
        #number of wedges for flickering checkerboards
        'numWedgePairs':8,
        #width of each ring for flickering checkerboards
        #defined here as 15 rings
        'ringWidth':1.0,
        #duration of stim A for arbitrary timing drifting checkerboards
        'stimDurationA':1,
        #duration of stim B for arbitrary timing drifting checkerboards
        'stimDurationB':1,
        #duration of in-block rest for arbitrary timing drifting checkerboards
        'stimDurationRest':1,
        #number of blocks for arbitrary timing drifting checkerboards
        'numBlocks':10,
        #number of A-B-rest reps per block for arbitrary timing drifting checkerboards
        'numReps':5,
        #duration of post-stim rest for arbitrary timing drifting checkerboards
        'postScanRest':12,

        }
    #get rid of numScans--it isn't used in dynamic mode
    if 'numScans' in scanDict:
        del scanDict['numScans']
    #make a little dictionary with the generic parameters needed for all scans
    scanDictAll=dict()
    scanDictAll['Tr']=scanDict['Tr']
    scanDictAll['innerRadius']=scanDict['innerRadius']
    scanDictAll['fixFraction']=scanDict['fixFraction']
    #scanDictAll['monitor']=scanDict['monitor']
    scanDictAll['operatorScreen']=scanDict['operatorScreen']
    scanDictAll['subjectScreen']=scanDict['subjectScreen']
    scanDictAll['trigger']=scanDict['trigger']
    scanDictAll['subjectResponse']=scanDict['subjectResponse']
    localMon=monitors.getAllMonitors()
    #create an ordered group to choose from, with the last-used monitor as the default choice
    myMonitorList=[]
    myMonitorList.append(scanDict['monitor'])
    myMonitorList.extend(localMon)
    #add the other local monitor choices
    scanDictAll['monitorChoices']=myMonitorList
    if thisPlatform==3:
        scanDictAll['operatorScreen']=0
        scanDictAll['subjectScreen']=0

    #either way, I have the dict. pop a gui
#     infoDlg=gui.DlgFromDict(dictionary=scanDict,title='Scan parameters',
#                             order=['Tr','numCycles','period','preScanRest','contrast','monitor','operatorScreen','subjectScreen','innerRadius','outerRadius','fixFraction','animFreq','pairWedge'],
#                             tip={'Tr':'seconds','numCycles':'number of cycles','period':'seconds',
#                                  'preScanRest':'seconds','contrast':'0 to 1','numScans':'will loop through this many times',
#                                  'monitor':'choose from 7T/PS, debug, other, 7T/AS',
#                                  'operatorScreen':'normally 0','subjectScreen':'normallly 1',
#                                  'innerRadius':'degrees','outerRadius':'degrees',
#                                  'fixFraction':'fraction of the time the fixation point could change',
#                                  #'wedgeWidth':'width of wedge (deg) for rotating wedge',
#                                  #'dutyCycle':'eccentricity width of ring (\%)',
#                                  'animFreq':'animation frequency, Hz (drift/flicker frequency)',
#                                  'pairWedge':'draw a second set of wedges on the opposite side (rotating wedges only); 0 o r1 (no/yes)'})
    if thisPlatform==2:
        fixedFields=['operatorScreen','subjectScreen']
    else:
        fixedFields=[]
    infoDlg=gui.DlgFromDict(dictionary=scanDictAll,title='Scan parameters',
                           order=['Tr','innerRadius','fixFraction','monitorChoices','operatorScreen','subjectScreen','trigger','subjectResponse'],
                            tip={'Tr':'seconds',
                                 'innerRadius':'degrees','outerRadius':'degrees',
                                 'fixFraction':'fraction of the time the fixation point could change',
                                 'monitorChoices':'choose from local monitors',
                                 'operatorScreen':'normally 0','subjectScreen':'normally 1',
                                 'trigger':'trigger character',
                                 'subjectResponse':'possible subject response characters',})
    if infoDlg.OK:
        print(scanDictAll)
        #copy the values back into the main dict
        scanDict['Tr']=scanDictAll['Tr']
        scanDict['innerRadius']=scanDictAll['innerRadius']
        scanDict['fixFraction']=scanDictAll['fixFraction']
        scanDict['monitor']=scanDictAll['monitorChoices']
        scanDict['operatorScreen']=scanDictAll['operatorScreen']
        scanDict['subjectScreen']=scanDictAll['subjectScreen']
        scanDict['trigger']=scanDictAll['trigger']
        scanDict['subjectResponse']=scanDictAll['subjectResponse']


        #running--save the params
        misc.toFile('lastrun.pickle',scanDict)
    else:
        print('user cancelled')
        core.quit()
    #root.deiconify()
else:
    print('user cancelled')
    core.quit()
#either way, set up the monitor
#monitor calibration information

print('scanDict monitor')
print(scanDict['monitor'])

#
# if 'new' in scanDict['monitor']:
#     #get the list of monitors and present a gui to choose
#     localMon=monitors.getAllMonitors()
#     myDlg = gui.Dlg(title="local monitor calibrations")
#     myDlg.addText('Choose the monitor calibration you want to use')
#     myDlg.addText('Your monitor must already have been setup in the Psychopy monitor center')
#     myDlg.addField('calibrations:', choices=localMon)
#     myDlg.show()  # show dialog and wait for OK or Cancel
#     if myDlg.OK:  # then the user pressed OK
#         scanDict['monCalFile']=myDlg.data[0]
#         mon=monitors.Monitor(myDlg.data[0])
#     else:
#         scanDict['monCalFile']='testMonitor'
#         mon=monitors.Monitor('testMonitor')


mon=monitors.Monitor(scanDict['monitor'])
#print("mon")
#print(mon)
scanDict['monCalFile']=scanDict['monitor']
# if '3TA' in scanDict['monitor']:
#     scanDict['monCalFile'] = '3TA'
#     mon=monitors.Monitor('3TA')
# if '3TB' in scanDict['monitor']:
#     scanDict['monCalFile'] = '3TB'
#     mon=monitors.Monitor('3TB')
# elif 'ASwest' in scanDict['monitor']:
#     #monCal = '7TAScaldate'
#     #monCal='ASrearProj'
#     scanDict['monCalFile']='7TASwest'
#     mon=monitors.Monitor('7TASwest')
# elif 'ASeast' in scanDict['monitor']:
#     #monCal = '7TAScaldate'
#     #monCal='ASrearProj'
#     scanDict['monCalFile']='7TASeast'
#     mon=monitors.Monitor('7TASeast')
# elif 'PS' in scanDict['monitor']:
#     scanDict['monCalFile']='7TPS'
#     mon=monitors.Monitor('7TPS')
# #    monCal = '7TPS20120921'
# elif 'debug' in scanDict['monitor']:
#     scanDict['monCalFile']='laptopSelfScreen'
#     mon=monitors.Monitor('laptopSelfScreen')
# elif 'new' in scanDict['monitor']:
#     #get the list of monitors and present a gui to choose
#     localMon=monitors.getAllMonitors()
#     myDlg = gui.Dlg(title="local monitor calibrations")
#     myDlg.addText('Choose the monitor calibration you want to use')
#     myDlg.addText('Your monitor must already have been setup in the Psychopy monitor center')
#     myDlg.addField('calibrations:', choices=localMon)
#     myDlg.show()  # show dialog and wait for OK or Cancel
#     if myDlg.OK:  # then the user pressed OK
#         scanDict['monCalFile']=myDlg.data[0]
#         mon=monitors.Monitor(myDlg.data[0])
#     else:
#         scanDict['monCalFile']='testMonitor'
#         mon=monitors.Monitor('testMonitor')
#
# else:
#     scanDict['monCalFile']='testMonitor'
#     mon=monitors.Monitor('testMonitor')

#check to see if the monitor file exists
localMon=monitors.getAllMonitors()
#returns a list. look through it
thisMon=scanDict['monCalFile']
if thisMon not in localMon:
    scanDict['monCalFile']='testMonitor'
    mon=monitors.Monitor('testMonitor')
    #print a warning
    print('Monitor not found; using built in testMonitor')

#
#if scanDict['operatorScreen']!= scanDict['subjectScreen']:
#    if 'AS' in scanDict['monCalFile']:
#        screenSize=[1600,1200]
#        screenSize=[1024,768]
#    else:
#        screenSize=[1024,768]
#else:
#    screenSize=[1024,768]
thisScreenSize=mon.getSizePix()
screenSize=thisScreenSize
scanDict['screenSize']=screenSize
#set the platform
scanDict['platform']=thisPlatform


#define which parameters go with which scan type
wedgeParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','wedgeWidth','animFreq','pairWedge','contrast','platform','screenSize','trigger','subjectResponse']
ringParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','dutyCycle','animFreq','contrast','platform','screenSize','trigger','subjectResponse']
motionParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','contrast','platform','screenSize','trigger','subjectResponse']
objectParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','platform','screenSize','trigger','subjectResponse']
flickParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','animFreq','colorA','colorB','colorBackground','timeBase','fixationStyle','platform','screenSize','trigger','subjectResponse','numWedgePairs','ringWidth']
flickarbParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','animFreq','colorA','colorB','colorBackground','stimDuration','fixationStyle','platform','screenSize','trigger','subjectResponse','numWedgePairs','ringWidth']
driftParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','period','numCycles','outerRadius','animFreq','contrast','platform','screenSize','trigger','subjectResponse']
driftArbParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','numBlocks','numReps','outerRadius','animFreq','contrast','platform','screenSize','trigger','subjectResponse','postScanRest','stimDurationA','stimDurationB','stimDurationRest']
drift3Params=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','animFreq','Ralpha','Rbeta','contrast','platform','screenSize','trigger','subjectResponse']
vwfaParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','platform','screenSize','trigger','subjectResponse']
achromParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','stimDuration','period','numCycles','outerRadius','animFreq','colorBackground','platform','screenSize','trigger','subjectResponse']
isolumParams=['monCalFile','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','preScanRest','period','numCycles','outerRadius','animFreq','colorA','colorB','colorBackground','timeBase','platform','screenSize','trigger','subjectResponse']


if scanMode==1:
    #for paramFile mode, the sequence of scans is set
    #backwards compatibility--rename flickFreq as animFreq
    if 'flickFreq' in scanDict:
        scanDict['animFreq']=scanDict['flickFreq']
        del scanDict['flickFreq']
    #loop through the scans and do each one
    for i in range(numScans):
        thisScan = scanSeq[i]
        if thisScan=='cw wedge':
            #call wedge, dir = +1
            runInfo = wedgeScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)
            #save something?
            #inform user?
        elif thisScan=='ccw wedge':
            #call wedge, dir = -1
            runInfo = wedgeScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)
        elif thisScan=='contracting ring':
            #call ring, dir = +1
            runInfo = ringScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)
        elif thisScan=='expanding ring':
            #call ring, dir = -1
            runInfo = ringScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)
        elif thisScan=='motionA':
            #call motion, dir = +1
            runInfo = motionScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)
        elif thisScan=='motionB':
            #call motion, dir = -1
            runInfo = motionScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)
        elif thisScan=='objectA':
            #call object, dir = +1
            runInfo = objectScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)
        elif thisScan=='objectB':
            #call object, dir = -1
            runInfo = objectScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)
        elif thisScan=='full-field flickering checkerboard':
            #get colors/flicker rate from file
            runInfo = flickerScan(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='full-field flickering checkerboard asymmetric':
            #get colors/flicker rate from file OR dialog
            runInfo = flickerScanArb(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='center-inner-outer checkerboard':
            #drift checker board with center, inner surround, outer surround
            runInfo = driftChecker3mask(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=3,maskType=1)
        elif thisScan=='drifting checkerboard on-off':
            #full field DRIFTING checkerboard, B&W
            runInfo = driftChecker(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=1)
        elif thisScan=='drifting checkerboard drift-static':
            #full field checkerboard, B&W, drift-vs-static
            runInfo = driftChecker(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=2)
        elif thisScan=='drifting checkerboard center-surround':
            #center surround checkerboard.......
            runInfo = driftChecker(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=3,maskType=1)
        elif thisScan=='drifting checkerboard alternating halves':
            #alternating halves checkerboard....
            runInfo = driftChecker(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=3,maskType=2)
        elif thisScan=='drifting checkerboard on-off asymmetric':
            #full field DRIFTING checkerboard, B&W
            runInfo = driftCheckerArb(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=1)
        elif thisScan=='drifting checkerboard drift-static asymmetric':
            #full field checkerboard, B&W, drift-vs-static
            runInfo = driftCheckerArb(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=2)
        elif thisScan=='drifting checkerboard center-surround asymmetric':
            #center surround checkerboard.......
            runInfo = driftCheckerArb(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=3,maskType=1)
        elif thisScan=='drifting checkerboard alternating halves asymmetric':
            #alternating halves checkerboard....
            runInfo = driftCheckerArb(scanDict = scanDict, screenSize=screenSize,offTimeBehavior=3,maskType=2)
        elif thisScan=='achromatic wedges':
            #get colors/flicker rate from file OR dialog
            runInfo = achromaticWedges(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='isoluminance test':
            #set red-green isoluminance values
            runInfo = isolumTest(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='isoluminant checkerboards':
            #need isoluminant red/green from test
            #get these from the file they're saved in....
            runInfo = isolumCheckerScan(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='VWFA localizer':
            #set red-green isoluminance values
            runInfo = VWFAloc(scanDict = scanDict, screenSize=screenSize)
        elif thisScan=='VWFA localizer images':
            #set red-green isoluminance values
            runInfo = VWFAlocImages(scanDict = scanDict, screenSize=screenSize)


elif scanMode==2:
    #dynamically choose the next scan
    #do this over and over until the user quits
    while True:

        #make an oldschool clickable image to choose the next scan type

        #draw a grid with all the scan types
        #define box corners for them all, FROM UPPER LEFT CORNER (later relative to center)
        boxCenter=(0,0)
        boxDims=(690,40)
        #create a scan types dictionary, so I can keep track of things
        scanTypes={}

        scanTypes['cw22.5']={'paramFileName':'cw wedge','boxC':[-200,260],'boxT':'CW rotating wedge, 22.5 deg'} #1
        scanTypes['ccw22.5']={'paramFileName':'ccw wedge','boxC':[-200,220],'boxT':'CCW rotating wedge, 22.5 deg'} #2
        scanTypes['cw45']={'paramFileName':'cw wedge','boxC':[-200,180],'boxT':'CW rotating wedge, 45 deg'} #3
        scanTypes['ccw45']={'paramFileName':'ccw wedge','boxC':[-200,140],'boxT':'CCW rotating wedge, 45 deg'} #4
        scanTypes['exp12.5']={'paramFileName':'expanding ring','boxC':[200,260],'boxT':'expanding ring, 12.5% duty'} #5
        scanTypes['con12.5']={'paramFileName':'contracting ring','boxC':[200,220],'boxT':'contracting ring, 12.5% duty'} #6
        scanTypes['exp25']={'paramFileName':'expanding ring','boxC':[200,180],'boxT':'expanding ring, 25% duty'} #7
        scanTypes['con25']={'paramFileName':'contracting ring','boxC':[200,140],'boxT':'contracting ring, 25% duty'} #8

        scanTypes['mtA']={'paramFileName':'motionA','boxC':[-200,60],'boxT':'moving dots (MT), drift-static'} #20
        scanTypes['mtB']={'paramFileName':'motionB','boxC':[-200,20],'boxT':'moving dots, static-drift'} #21
        scanTypes['LOCA']={'paramFileName':'objectA','boxC':[-200,-20],'boxT':'intact vs scrambled objects (LOC)'} #22
        scanTypes['LOCB']={'paramFileName':'objectB','boxC':[-200,-60],'boxT':'scrambled vs intact objects'} #23
        scanTypes['VWFA']={'paramFileName':'VWFA localizer','boxC':[200,20],'boxT':'VWFA: faces, houses, chairs, letters'} #15

        scanTypes['flickOnOff']={'paramFileName':'full-field flickering checkerboard','boxC':[-200,-140],'boxT':'flickering checkerboard, on-off'} #18
        scanTypes['flickAsym']={'paramFileName':'full-field flickering checkerboard asymmetric','boxC':[200,-140],'boxT':'flickering, asymmetric timing'} #19

        scanTypes['driftOnOff']={'paramFileName':'drifting checkerboard on-off','boxC':[-200,-220],'boxT':'drifting, full field, on-off'} #9
        scanTypes['driftDriftStatic']={'paramFileName':'drifting checkerboard drift-static','boxC':[-200,-260],'boxT':'full-field, drift-static'} #10
        scanTypes['driftCenterSurr']={'paramFileName':'drifting checkerboard center-surround','boxC':[-200,-300],'boxT':'center-surround'} #11
        scanTypes['driftAltHalves']={'paramFileName':'drifting checkerboard alternating halves','boxC':[-200,-340],'boxT':'alternating halves'} #12
        scanTypes['driftCenterInnerOuter']={'paramFileName':'center-inner-outer checkerboard','boxC':[-200,-380],'boxT':'center/inner/outer surround'} #13
        scanTypes['driftOnOffArb']={'paramFileName':'drifting checkerboard on-off asymmetric','boxC':[200,-220],'boxT':'drifting, full field, on-off, asymmetric timing'} #9
        scanTypes['driftDriftStaticArb']={'paramFileName':'drifting checkerboard drift-static asymmetric','boxC':[200,-260],'boxT':'full-field, drift-static, asymmetric timing'} #10
        scanTypes['driftCenterSurrArb']={'paramFileName':'drifting checkerboard center-surround asymmetric','boxC':[200,-300],'boxT':'center-surround, asymmetric timing'} #11
        scanTypes['driftAltHalvesArb']={'paramFileName':'drifting checkerboard alternating halves asymmetric','boxC':[200,-340],'boxT':'alternating halves, asymmetric timing'} #12

        boxLabels={}
        boxLabels['choose']={'boxC':[0,340],'boxT':'choose the next scan type'}
        boxLabels['ret']={'boxC':[0,300],'boxT':'retinotopic mapping'}
        boxLabels['loc']={'boxC':[0,100],'boxT':'visual area localizers'}
        boxLabels['flick']={'boxC':[0,-100],'boxT':'flickering checkerboards'}
        boxLabels['drift']={'boxC':[0,-180],'boxT':'drifting checkerboards'}
        boxLabels['quit']={'boxC':[0,-420],'boxT':'QUIT'}

        #now draw boxes for each

        win=visual.Window([800,860],monitor='testMonitor',units='pix',screen=0,color=[0,0,0],colorSpace='rgb')

        myRect=visual.Rect(win,units='pix',lineColor=[0.3, 0.3, 0.3], lineColorSpace='rgb')
        myText=visual.TextStim(win,text='CW rotating wedge, 22.5 deg',pos=boxCenter,alignText='center',anchorVert='center')
        myMouse=event.Mouse(visible=True,win=win)
        for key in scanTypes:
            myRect.size=boxDims
            thing=scanTypes[key]['boxC']
            myRect.pos=thing
            myText.pos=(scanTypes[key]['boxC'][0],scanTypes[key]['boxC'][1]+3)
            myText.setText(scanTypes[key]['boxT'])
            myRect.draw()
            myText.draw()
        for key in boxLabels:
            myRect.size=(boxDims[0]*2,boxDims[1])
            myRect.pos=boxLabels[key]['boxC']
            myText.pos=(boxLabels[key]['boxC'][0],boxLabels[key]['boxC'][1]+3)
            myText.setText(boxLabels[key]['boxT'])
            myRect.draw()
            myText.draw()
        win.flip()

        #wait for a mouse click event

        #get the next scan type based on mouse position
        myMouse.clickReset()
        choice=0
        while choice==0:
            buttons=myMouse.getPressed()
            click=buttons[0]
            loc=myMouse.getPos()
            if click==1:
                #print loc
                #check if the click was in a valid place
                myRect.size=boxDims
                myRect.pos=boxLabels['quit']['boxC']
                quitBox=myRect.contains(loc)
                if quitBox==1:
                    core.quit()
                for key in scanTypes:
                    myRect.size=boxDims
                    myRect.pos=scanTypes[key]['boxC']
                    thisBox=myRect.contains(loc)
                    if thisBox==1:
                        choice=key


        nextScanType=choice
        win.close()


        if nextScanType=='cw22.5':
            #CW wedge, 22.5 degrees
            scanDict['wedgeWidth']=22.5
            #make a new dict with only the relevant params
            scanDictWedge=dict([(i,scanDict[i]) for i in wedgeParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictWedge,title='Wedge parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq', 'pairWedge','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz', 'pairWedge':'0 (off) or 1 (on)','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictWedge
                #copy values back to main dict
                for iParam in scanDictWedge.keys():
                    scanDict[iParam]=scanDictWedge[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunwedgeScan.pickle',scanDictWedge)
            else:
                print('user cancelled')
                core.quit()
            runInfo = wedgeScan(scanDict = scanDictWedge, screenSize = screenSize, direction = 1.0)

        elif nextScanType=='ccw22.5':
            #CCW wedge, 22.5 degrees
            scanDict['wedgeWidth']=22.5
            #make a new dict with only the relevant params
            scanDictWedge=dict([(i,scanDict[i]) for i in wedgeParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictWedge,title='Wedge parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq', 'pairWedge','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz', 'pairWedge':'0 (off) or 1 (on)','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictWedge
                #copy values back to main dict
                for iParam in scanDictWedge.keys():
                    scanDict[iParam]=scanDictWedge[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunwedgeScan.pickle',scanDictWedge)
            else:
                print('user cancelled')
                core.quit()
            runInfo = wedgeScan(scanDict = scanDictWedge, screenSize = screenSize, direction = -1.0)

        elif nextScanType=='cw45':
            #CW wedge, 45 degrees
            scanDict['wedgeWidth']=45
            #make a new dict with only the relevant params
            scanDictWedge=dict([(i,scanDict[i]) for i in wedgeParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictWedge,title='Wedge parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq', 'pairWedge','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz', 'pairWedge':'0 (off) or 1 (on)','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictWedge
                #copy values back to main dict
                for iParam in scanDictWedge.keys():
                    scanDict[iParam]=scanDictWedge[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunwedgeScan.pickle',scanDictWedge)
            else:
                print('user cancelled')
                core.quit()
            runInfo = wedgeScan(scanDict = scanDictWedge, screenSize = screenSize, direction = 1.0)


        elif nextScanType=='ccw45':
            #CCW wedge, 45 degrees
            scanDict['wedgeWidth']=45
            #make a new dict with only the relevant params
            scanDictWedge=dict([(i,scanDict[i]) for i in wedgeParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictWedge,title='Wedge parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq', 'pairWedge','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz', 'pairWedge':'0 (off) or 1 (on)','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictWedge
                #copy values back to main dict
                for iParam in scanDictWedge.keys():
                    scanDict[iParam]=scanDictWedge[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunwedgeScan.pickle',scanDictWedge)
            else:
                print('user cancelled')
                core.quit()
            runInfo = wedgeScan(scanDict = scanDictWedge, screenSize = screenSize, direction = -1.0)


        elif nextScanType=='exp12.5':
            #expanding ring, 12.5% duty cycle
            scanDict['dutyCycle']=12.5
            #make a new dict with only the relevant params
            scanDictRing=dict([(i,scanDict[i]) for i in ringParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictRing,title='Ring parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictRing
                #copy values back to main dict
                for iParam in scanDictRing.keys():
                    scanDict[iParam]=scanDictRing[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunringScan.pickle',scanDictRing)
            else:
                print('user cancelled')
                core.quit()
            runInfo = ringScan(scanDict = scanDictRing, screenSize = screenSize, direction = -1.0)


        elif nextScanType=='con12.5':
            #contracting ring, 12.5% duty cycle
            scanDict['dutyCycle']=12.5
            #make a new dict with only the relevant params
            scanDictRing=dict([(i,scanDict[i]) for i in ringParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictRing,title='Ring parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictRing
                #copy values back to main dict
                for iParam in scanDictRing.keys():
                    scanDict[iParam]=scanDictRing[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunringScan.pickle',scanDictRing)
            else:
                print('user cancelled')
                core.quit()
            runInfo = ringScan(scanDict = scanDictRing, screenSize = screenSize, direction = 1.0)



        elif nextScanType=='exp25':
            #expanding ring, 25% duty cycle
            scanDict['dutyCycle']=25
            #make a new dict with only the relevant params
            scanDictRing=dict([(i,scanDict[i]) for i in ringParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictRing,title='Ring parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius','contrast', 'animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictRing
                #copy values back to main dict
                for iParam in scanDictRing.keys():
                    scanDict[iParam]=scanDictRing[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunringScan.pickle',scanDictRing)
            else:
                print('user cancelled')
                core.quit()
            runInfo = ringScan(scanDict = scanDictRing, screenSize = screenSize, direction = -1.0)



        elif nextScanType=='con25':
            #contracting ring, 25% duty cycle
            scanDict['dutyCycle']=25
            #make a new dict with only the relevant params
            scanDictRing=dict([(i,scanDict[i]) for i in ringParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictRing,title='Ring parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius','contrast', 'animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictRing
                #copy values back to main dict
                for iParam in scanDictRing.keys():
                    scanDict[iParam]=scanDictRing[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunringScan.pickle',scanDictRing)
            else:
                print('user cancelled')
                core.quit()
            runInfo = ringScan(scanDict = scanDictRing, screenSize = screenSize, direction = 1.0)



        elif nextScanType=='driftOnOff':
            #full field DRIFTING checkerboard, B&W, on/off
            #make a new dict with only the relevant params
            scanDictDrift=dict([(i,scanDict[i]) for i in driftParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDrift,title='Drifting Checkerboard parameters',
                                        order = ['period', 'numCycles', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDrift.keys():
                    scanDict[iParam]=scanDictDrift[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDrift)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftChecker(scanDict = scanDictDrift, screenSize=screenSize,offTimeBehavior=1)


        elif nextScanType=='driftDriftStatic':
            #full field checkerboard, B&W, drift-vs-static
            #make a new dict with only the relevant params
            scanDictDrift=dict([(i,scanDict[i]) for i in driftParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDrift,title='Drifting Checkerboard parameters',
                                        order = ['period', 'numCycles', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDrift.keys():
                    scanDict[iParam]=scanDictDrift[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDrift)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftChecker(scanDict = scanDictDrift, screenSize=screenSize,offTimeBehavior=2)


        elif nextScanType=='driftCenterSurr':
            #center surround checkerboard.......
            #make a new dict with only the relevant params
            scanDictDrift=dict([(i,scanDict[i]) for i in driftParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDrift,title='Drifting Checkerboard parameters',
                                        order = ['period', 'numCycles', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDrift.keys():
                    scanDict[iParam]=scanDictDrift[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDrift)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftChecker(scanDict = scanDictDrift, screenSize=screenSize,offTimeBehavior=3,maskType=1)


        elif nextScanType=='driftAltHalves':
            #alternating halves checkerboard....
            #make a new dict with only the relevant params
            scanDictDrift=dict([(i,scanDict[i]) for i in driftParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDrift,title='Drifting Checkerboard parameters',
                                        order = ['period', 'numCycles', 'outerRadius','contrast', 'animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'period':'seconds', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDrift.keys():
                    scanDict[iParam]=scanDictDrift[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDrift)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftChecker(scanDict = scanDictDrift, screenSize=screenSize,offTimeBehavior=3,maskType=2)


        elif nextScanType=='driftCenterInnerOuter':
            #center/innersurround/outersurround checkerboard.......
            scanDict['Ralpha']=1.0
            scanDict['Rbeta']=2.0

            #make a new dict with only the relevant params
            scanDictDrift3=dict([(i,scanDict[i]) for i in drift3Params if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDrift3,title='Drifting Checkerboard parameters',
                                        order = ['preScanRest', 'period', 'numCycles','contrast', 'Ralpha','Rbeta','outerRadius', 'animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'Ralpha':'border of center and inner surround','Rbeta':'border of inner surround and outer surround','outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift3
                #copy values back to main dict
                for iParam in scanDictDrift3.keys():
                    scanDict[iParam]=scanDictDrift3[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundrift3Scan.pickle',scanDictDrift3)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftChecker3mask(scanDict = scanDictDrift3, screenSize=screenSize,offTimeBehavior=3,maskType=1)


        elif nextScanType=='driftOnOffArb':
            #full field DRIFTING checkerboard, B&W, on/off
            #make a new dict with only the relevant params
            scanDictDriftArb=dict([(i,scanDict[i]) for i in driftArbParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDriftArb,title='Drifting Checkerboard Arb parameters',
                                        order = ['preScanRest','numBlocks','numReps','stimDurationA','stimDurationB','stimDurationRest','postScanRest', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'numBlocks':'number of A-B-rest blocks','numReps':'Number of A-B reps per block', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )

            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDriftArb.keys():
                    scanDict[iParam]=scanDictDriftArb[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScanArb.pickle',scanDictDriftArb)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftCheckerArb(scanDict = scanDictDriftArb, screenSize=screenSize,offTimeBehavior=1)


        elif nextScanType=='driftDriftStaticArb':
            #full field checkerboard, B&W, drift-vs-static
            #make a new dict with only the relevant params
            scanDictDriftArb=dict([(i,scanDict[i]) for i in driftArbParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDriftArb,title='Drifting Checkerboard Arb parameters',
                                        order = ['preScanRest','numBlocks','numReps','stimDurationA','stimDurationB','stimDurationRest','postScanRest', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'numBlocks':'number of A-B-rest blocks','numReps':'Number of A-B reps per block', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )

            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDriftArb.keys():
                    scanDict[iParam]=scanDictDriftArb[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDriftArb)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftCheckerArb(scanDict = scanDictDriftArb, screenSize=screenSize,offTimeBehavior=2)


        elif nextScanType=='driftCenterSurrArb':
            #center surround checkerboard.......
            #make a new dict with only the relevant params
            scanDictDriftArb=dict([(i,scanDict[i]) for i in driftArbParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDriftArb,title='Drifting Checkerboard Arb parameters',
                                        order = ['preScanRest','numBlocks','numReps','stimDurationA','stimDurationB','stimDurationRest','postScanRest', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'numBlocks':'number of A-B-rest blocks','numReps':'Number of A-B reps per block', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )

            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDriftArb.keys():
                    scanDict[iParam]=scanDictDriftArb[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDriftArb)
            else:
                print('user cancelled')
                core.quit()
            runInfo = driftCheckerArb(scanDict = scanDictDriftArb, screenSize=screenSize,offTimeBehavior=3,maskType=1)


        elif nextScanType=='driftAltHalvesArb':
            #alternating halves checkerboard....
            #make a new dict with only the relevant params
            scanDictDriftArb=dict([(i,scanDict[i]) for i in driftArbParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictDriftArb,title='Drifting Checkerboard Arb parameters',
                                        order = ['preScanRest','numBlocks','numReps','stimDurationA','stimDurationB','stimDurationRest','postScanRest', 'outerRadius', 'contrast','animFreq','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'numBlocks':'number of A-B-rest blocks','numReps':'Number of A-B reps per block', 'outerRadius':'degrees', 'animFreq':'Hz','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictDrift
                #copy values back to main dict
                for iParam in scanDictDriftArb.keys():
                    scanDict[iParam]=scanDictDriftArb[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrundriftScan.pickle',scanDictDriftArb)
            else:
                print('user cancelled')
                core.quit()
            print(screenSize)
            runInfo = driftCheckerArb(scanDict = scanDictDriftArb, screenSize=screenSize,offTimeBehavior=3,maskType=2)


        elif nextScanType=='VWFAemot':
            #VWFA localizer. letters vs wingdings vs emoticons....
            #make a new dict with only the relevant params
            scanDictVWFA=dict([(i,scanDict[i]) for i in vwfaParams if i in scanDict])
            #copy values back to main dict
            for iParam in scanDictVWFA.keys():
                scanDict[iParam]=scanDictVWFA[iParam]

            misc.toFile('lastrun.pickle',scanDict)
            misc.toFile('lastrunvwfaScan.pickle',scanDictVWFA)
            runInfo = VWFAloc(scanDict = scanDictVWFA, screenSize=screenSize)


        elif nextScanType=='VWFA':
            #VWFA localizer. chairs vs houses vs faces vs letters...
            scanDictVWFA=dict([(i,scanDict[i]) for i in vwfaParams if i in scanDict])
            for iParam in scanDictVWFA.keys():
                scanDict[iParam]=scanDictVWFA[iParam]

            misc.toFile('lastrun.pickle',scanDict)
            misc.toFile('lastrunvwfaScan.pickle',scanDictVWFA)
            runInfo = VWFAlocImages(scanDict = scanDictVWFA, screenSize=screenSize)


        elif nextScanType=='isolumTest':
            #test red-green for isoluminance
            scanDictIsolum=dict([(i,scanDict[i]) for i in isolumParams if i in scanDict])
            for iParam in scanDictIsolum.keys():
                scanDict[iParam]=scanDictIsolum[iParam]

            misc.toFile('lastrun.pickle',scanDict)
            misc.toFile('lastrunisolumScan.pickle',scanDictIsolum)
            runInfo = isolumTest(scanDict = scanDictIsolum, screenSize=screenSize)


        elif nextScanType=='isolum':
            #isoluminant red-green checkerboards
            scanDictIsolum=dict([(i,scanDict[i]) for i in isolumParams if i in scanDict])
            #need to load isoluminant values from the pickle from the test scan
            #for now, hard code them
            scanDict['red']=255
            scanDict['green']=128
            scanDict['colorA']=[1,0,0]
            scanDict['colorB']=[0,0.5,0]
            scanDict['colorBackground']=[0.5,0.5,0.5],
            scanDict['timeBase']=1

            for iParam in scanDictIsolum.keys():
                scanDict[iParam]=scanDictIsolum[iParam]

            misc.toFile('lastrun.pickle',scanDict)
            misc.toFile('lastrunisolumScan.pickle',scanDictIsolum)
            runInfo = isolumCheckerScan(scanDict = scanDictIsolum, screenSize=screenSize)


        elif nextScanType=='flickOnOff':
            #flickering checkerboard....
            scanDictFlick=dict([(i,scanDict[i]) for i in flickParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictFlick,title='Flickering checkerboard parameters',
            order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'fixationStyle','animFreq','colorA','colorB','colorBackground','numWedgePairs','ringWidth','timeBase','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
            fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
            tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'fixationStyle':'1 for rotation, 2 for rotation and color change','animFreq':'Hz','colorA':'RGB triplet, 0-1 for each','colorB':'RGB triplet, 0-1 for each','colorBackground':'RGB triplet, 0-1 for each','timeBase':'1 (time based) or 0 (trigger based)','numWedgePairs':'number of wedges','ringWidth':'width of each ring (deg)'}
            )
            if infoDlg.OK:
#                print scanDictFlick
                for iParam in scanDictFlick.keys():
                    scanDict[iParam]=scanDictFlick[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunflickScan.pickle',scanDictFlick)
            else:
                print('user cancelled')
                core.quit()
            runInfo = flickerScan(scanDict = scanDictFlick, screenSize=screenSize)


        elif nextScanType=='flickAsym':
            #flickering checkerboard with asymmetric timing....
            scanDictFlickarb=dict([(i,scanDict[i]) for i in flickarbParams if i in scanDict])
            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictFlickarb,title='Flickering checkerboard parameters',
            order = ['preScanRest', 'stimDuration','period', 'numCycles', 'outerRadius', 'fixationStyle','animFreq','colorA','colorB','colorBackground','numWedgePairs','ringWidth','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
            fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
            tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees', 'fixationStyle':'1 for rotation, 2 for rotation and color change','animFreq':'Hz','colorA':'RGB triplet, 0-1 for each','colorB':'RGB triplet, 0-1 for each','colorBackground':'RGB triplet, 0-1 for each','stimDuration':'seconds','numWedgePairs':'number of wedges','ringWidth':'width of each ring (deg)'}
            )
            if infoDlg.OK:
#                print scanDictFlickarb
                for iParam in scanDictFlickarb.keys():
                    scanDict[iParam]=scanDictFlickarb[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunflickarbScan.pickle',scanDictFlickarb)
            else:
                print('user cancelled')
                core.quit()
            runInfo = flickerScanArb(scanDict = scanDictFlickarb, screenSize=screenSize)


        elif nextScanType=='mtA':
            #MT direction A (drift-static)
            #make a new dict with only the relevant params
            scanDictMotion=dict([(i,scanDict[i]) for i in motionParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictMotion,title='Motion (A) parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictMotion
                #copy values back to main dict
                for iParam in scanDictMotion.keys():
                    scanDict[iParam]=scanDictMotion[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunmotionScan.pickle',scanDictMotion)
            else:
                print('user cancelled')
                core.quit()
            runInfo = motionScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)

        elif nextScanType=='mtB':
            #MT direction B (static-drift)
            #make a new dict with only the relevant params
            scanDictMotion=dict([(i,scanDict[i]) for i in motionParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictMotion,title='Motion (B) parameters',
                                        order = ['preScanRest', 'period', 'numCycles', 'outerRadius', 'contrast','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds', 'outerRadius':'degrees','contrast':'0 to 1'}
                                        )
            if infoDlg.OK:
#                print scanDictMotion
                #copy values back to main dict
                for iParam in scanDictMotion.keys():
                    scanDict[iParam]=scanDictMotion[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunmotionScan.pickle',scanDictMotion)
            else:
                print('user cancelled')
                core.quit()
            runInfo = motionScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)

        elif nextScanType=='LOCA':
            #LOC direction A (intact-scrambled)
            #make a new dict with only the relevant params
            scanDictObject=dict([(i,scanDict[i]) for i in objectParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictObject,title='Motion parameters',
                                        order = ['preScanRest', 'period', 'numCycles','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds'}
                                        )
            if infoDlg.OK:
#                print scanDictObject
                #copy values back to main dict
                for iParam in scanDictObject.keys():
                    scanDict[iParam]=scanDictObject[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunobjectScan.pickle',scanDictObject)
            else:
                print('user cancelled')
                core.quit()
            runInfo = objectScan(scanDict = scanDict, screenSize = screenSize, direction = 1.0)

        elif nextScanType=='LOCB':
            #LOC direction B (scrambled-intact)
            #make a new dict with only the relevant params
            scanDictObject=dict([(i,scanDict[i]) for i in objectParams if i in scanDict])

            #pop a GUI to confirm/update values
            infoDlg = gui.DlgFromDict(dictionary=scanDictObject,title='Motion parameters',
                                        order = ['preScanRest', 'period', 'numCycles','Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen'],
                                        fixed=['Tr','innerRadius','fixFraction','monitor','operatorScreen','subjectScreen','monitor','monCalFile','platform','screenSize','trigger','subjectResponse'],
                                        tip={'preScanRest':'seconds', 'period':'seconds'}
                                        )
            if infoDlg.OK:
#                print scanDictObject
                #copy values back to main dict
                for iParam in scanDictObject.keys():
                    scanDict[iParam]=scanDictObject[iParam]

                misc.toFile('lastrun.pickle',scanDict)
                misc.toFile('lastrunobjectScan.pickle',scanDictObject)
            else:
                print('user cancelled')
                core.quit()
            runInfo = objectScan(scanDict = scanDict, screenSize = screenSize, direction = -1.0)



        elif nextScanType==98:
            #swap screens
            #swap screen numbers
            oldOp=scanDict['operatorScreen']
            oldSub=scanDict['subjectScreen']
            scanDict['operatorScreen']=oldSub
            scanDict['subjectScreen']=oldOp
        elif nextScanType==99:
            core.quit()

core.quit()
