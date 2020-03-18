# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:15:40 2013

@author: agrant
"""

#!/usr/bin/env python
from psychopy import visual, event, core
import numpy
globalClock = core.Clock()
win = visual.Window([1024,768],monitor='testMonitor',units='deg',screen=1)

rect=visual.Rect(win,width=0.125,height=2,units='norm',pos=(-1,-1),fillColor=-1,fillColorSpace='rgb')
rect.setLineColor(None)

##make two wedges (in opposite contrast) and alternate them for flashing
#ring1 = visual.RadialStim(win, tex='sqrXsqr', color=[1,1,1],size=10,
#     mask=[0,0,1,1,0,0,0,0,0,0,], radialCycles=5, angularCycles=8,
#     interpolate=False)
t=0
rotationRate = 0.01 #revs per sec
driftRate=0.1

#ring1.setMask([1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,])
screenColors=numpy.linspace(-1,1,16)
segEdges=numpy.linspace(-1,1,17)+1.0/16.0

while t>-1:#for 5 secs
     t=globalClock.getTime()
     #ring1.setRadialPhase(t*driftRate)
     #ring1.setOri(t*rotationRate*360.0)

     #ring1.draw()
     for iSeg in range (0,16):
         rect.setFillColor(screenColors[iSeg])
         rect.setPos([segEdges[iSeg],0])
         rect.draw()
#     ring2.setOri(-t*rotationRate*360.0)
#     ring2.draw()
     win.flip()

     for key in event.getKeys():
         if key in ['q','escape']:
             core.quit()


win.close()