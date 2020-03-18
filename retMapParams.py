#create a dictionary with the scan parameters. Leave default info for(or delete) ones you don't need, need a comma after each pair except for the final pair
#'keyName':keyValue
scanDict={
#Tr (s)
'Tr':1.5,
#number of cycles (traveling wave cycle or stim-rest pairs)
'numCycles':10,
#period (s) of each cycle
'period':24,
#pre-scan duration (s) --rest before start OR traveling wave to show during throw-away time
'preScanRest':12,
#contrast for retinotopy, 0 to 1
'contrast':1.0,
# number of scans
'numScans':6,
#inner radius of stimulus (degrees)
'innerRadius':0.5,
#outer radius of stimulus (degrees)
'outerRadius':12.0,
#Monitor calibration filename
#choices are: 7T/AS    3T   7T/PS   debug   other
'monitor':'7T/PS',
#screen number for operator (normally 0 unless Yedi gets confused)
'operatorScreen':0,
#screen number for subject (normally 1)
'subjectScreen':1,
#fraction of time the fixation point could change
'fixFraction':0.2,
#stim duration (s) for on/off type scans--ignored for traveling waves
'stimDuration':5,
#colors and drift frequency for checkerboards
#color A of checkerboard, as RGB triplet (0 to 1 for each)
'colorA':[1,0,0],
#color B of checkerboard, as RGB triplet (0 to 1 for each)
'colorB':[0,0,0],
#background color for checkerboards as RGB triplet (0 to 1 for each)
'colorBackground':[0.1,0.1,0.1],
#flicker frequency (Hz) for checkerboards
'flickFreq':8,
#control scan timing via clocktime (1) or scanner triggers (0)
'timeBase':1
}

#scan sequence--initialize the variable for the number of scans
scanSeq = [0]*scanDict['numScans']
#choices are:
# cw wedge
# ccw wedge
# contracting ring
# expanding ring
# motionA
# motionB
# objectA
# objectB
# full-field flickering checkerboard
#
#for each scan, add the scan name
scanSeq[0]='cw wedge'
scanSeq[1]='ccw wedge'
scanSeq[2]='cw wedge'
scanSeq[3]='ccw wedge'
scanSeq[4]='expanding ring'
scanSeq[5]='contracting ring'
