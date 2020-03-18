#declare my list
scanInfo=[1,2,3,4,5,6,7,8,9,10,11]
#set the values in it
#Tr (s)
scanInfo[0]=5
#number of cycles (traveling wave cycle or stim-rest pairs)
scanInfo[1]=2
#period (s) of each cycle
scanInfo[2]=20
#pre-scan duration (s) --rest before start OR traveling wave to show during throw-away time
scanInfo[3]=20
#contrast for retinotopy, 0 to 1
scanInfo[4]=1.0
# number of scans
scanInfo[5]=1
# stimulus on external monitor (Y/N)
scanInfo[6]='Y'
#Monitor calibration filename
#choices are: 7T/AS    3T   7T/PS   debug   other
scanInfo[7]='7T/AS'
#screen number for operator (normally 0 unless Yedi gets confused)
scanInfo[8]=0
#screen number for subject (normally 1)
scanInfo[9]=1
#fraction of time the fixation point could change
scanInfo[10]=0.2

#scan sequence
scanSeq = [0]*scanInfo[5]
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
scanSeq[0]='full-field flickering checkerboard'

#colors and drift frequency
colors=[0]*5
#color A of checkerboard, as RGB triplet (0 to 1 for each)
colors[0]=[1,0,0]
#color A of checkerboard, as RGB triplet (0 to 1 for each)
colors[1]=[0,0,0]
#background color as RGB triplet
colors[2]=[0.1,0.1,0.1]
#flicker frequency (Hz)
colors[3]=8
#advance via time (1) or triggers (0)
colors[4]=0