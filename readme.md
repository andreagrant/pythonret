# Retinotopy stimulus package

## An apology
I wrote this code in 2012 when I was teaching myself python. At the time I :gasp: didn't even know what object oriented programming was. Like many scientists, I am self-taught as a programmer and had mostly written non-fancy c code and then MATLAB. So, this may be the most un-pythonic, procedural example of python you come across!

## retinotopy.py documentation
This program presents basic retinotopic mapping stimulus, localizers for MT (motion), LOC (objects), and VWFA (words) and a variety of flickering or drifting checkerboards. It reproduces the functions of the RET code which runs on Macs only. Retinotopy.py is a python script that uses the PsychoPy toolbox. For each scan, the code will wait for the subject to press a button indicating they are ready, then the code will wait for a trigger from the scanner. Some scans will present a third message to the operato before the ''subject ready'' message; this includes information about the length of the scan and number of TRs. The code expects keyboard presses for subject responses and trigger; the defaults are <i><b>bygr</i></b> for subject responses and <i><b>t</i></b> for trigger or <i><b>1234</i></b> for responses and <i><b>5</i></b> for trigger.

## Required citation
If you use the stimuli in a publication, please cite the papers describing <a href=&quot;http://www.psychopy.org/&quot;>PsychoPy</a>:
- Peirce, JW (2007) PsychoPy - Psychophysics software in Python. J Neurosci Methods, 162(1-2):8-13
- Peirce JW (2009) Generating stimuli for neuroscience using PsychoPy. Front. Neuroinform. 2:10. doi:10.3389/neuro.11.010.2008

The stimuli that use images have further citations (see ''Stimulus Types''); these are not available outside the CMRR, as I do not have rights to redistribute the processed images.

## Contact information
Andrea Grant, gran0260@umn.edu

## Running modes
- [Note: I believe this mode no longer works]: Predetermined scan sequence and timing details using a parameter file (details below)
- Run "dynamically" by choosing the timing information and other details, then choosing each scan type after the previous scan finishes

## Stimulus Types
1. Rotating wedge (drifting checkerboard).
   1. Wedge can be any width (22.5 and 45 are defaults)
   2. can rotate clockwise or counterclockwise
2. Expanding/contracting ring (drifting checkerboard).
   1. The ring can be any duty cycle (12.5% or 25% are defaults)
   2. can expand or contract
3. Motion localizer (field of drifting vs. static dots).
        - The scan can start with moving or static dots
4. Object localizer (intact vs. scrambled images).
   1. The scan can start with the intact or scrambled images.
   2. Note: the scrambled images are available but still need some optimization.
   3. **required citation**: images are from <a href="http://stims.cnbc.cmu.edu/Image%20Databases/TarrLab/Objects/">Tarr Lab</a>: " If you use any of these images in publicly available work - talks, papers, etc. - you must acknowledge their source and adhere to the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. You must also include the line Stimulus images courtesy of Michael J. Tarr, Center for the Neural Basis of Cognition and Department of Psychology, Carnegie Mellon University, http://www.tarrlab.org/."
5. Full field flickering checkerboard.
   1. Both checkerboard colors (and background color) and flicker frequency can be specified.
   2. Timing can be symmetric (X seconds on, X seconds off) or asymmetric
6. Full field drifting checkerboard (black and white on gray background)
   1. Stimulus on vs. off
   2. Drifting checkerboard vs. static checkerboard
   3. Center vs. surround checkerboard
   4. Center vs. inner surround vs. outer surround checkerboard (i.e., fovea vs. periphery localizer)
   5. Alternating halves checkerboard
   6. Timing can be symmetric (X seconds A, X seconds B) or asymmetric (X seconds A Y seconds B repeated N times followed by a rest of M. This block can be repeated)
7. Visual word form area (VWFA) localizer
   1. with images of words, chairs, houses, and faces in a block design (10 trials per block, 4 blocks of each type)
      - **required citations**:
         - faces are from <a href="http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html">AT&T Laboratories Cambridge</a>: "When using these images, please give credit to AT&T Laboratories Cambridge."
         - chairs and objects are from <a href="http://stims.cnbc.cmu.edu/Image%20Databases/TarrLab/Objects/">Tarr Lab</a>: " If you use any of these images in publicly available work - talks, papers, etc. - you must acknowledge their source and adhere to the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. You must also include the line Stimulus images courtesy of Michael J. Tarr, Center for the Neural Basis of Cognition and Department of Psychology, Carnegie Mellon University, http://www.tarrlab.org/."
         - houses are from <a href="http://groups.csail.mit.edu/vision/SUN/">MIT SUN database</a>:"SUN Database: Large-scale Scene Recognition from Abbey to Zoo". J. Xiao, J. Hays, K. Ehinger, A. Oliva, and A. Torralba. IEEE Conference on Computer Vision and Pattern Recognition, 2010.
   2. with letters, emoticons, and ''wingdings'' (letter-like but non-letter symbols) in a block design (12 trials per block, 3 blocks of each type)
      1. Note: the emoticons and wingdings don't display correctly yet

## Parameter File (may not work)
### Overview
The parameter file defines two variables that are used to control the stimuli. The first is a python &quot;dictionary&quot;, a series of key:value pairs. Some key/values aren't used for some stimuli; they can be removed from the parameter file or left in (and will be ignored). The format for a dictionary is myDict = {'key1':value1,'key2':value2}
- The key is in single quotes.
- If the value is a single number, just type the number:  <b>6.7</b>
- If it's a sequence of numbers, such as an RGB triplet, enclose it in square brackets separated by commas:  <b>[1,1,0]</b>
- If the value is a string, such as the monitor calibration name, enter it inside a pair of single quotes: <b>'7TASwest'</b>
- The key/value pairs can be in any order within the {} and are separated by a comma

The second variable is a "list" containing the stimulus types to be displayed, in order (# indicates the text following it will be ignored as a comment). The name of the stimulus type has to be entered exactly. The list is first declared to be the right length (don't edit this line)
- scanSeq = [0]*scanDict['numScans']
Then the individual scans are assigned:
- scanSeq[0]='full-field flickering checkerboard asymmetric'
- scanSeq[1]='cw wedge'
- scanSeq[2]='motionA'

### List of stimulus types and their official names in the parameter file
- <b>cw wedge:</b>&nbsp;&nbsp;&nbsp;wedge rotating clockwise. Rotation speed is determined by the period, drift speed (of the internal wedge bits, normally 0.2Hz) is set by animFreq, wedge width is set by wedgeWidth. This is a travelling wave retinotopy scan
- <b>ccw wedge:</b>&nbsp;&nbsp;&nbsp;wedge rotating counterclockwise. Rotation speed is determined by the period, drift speed (of the internal wedge bits, normally 0.2Hz) is set by animFreq, wedge width is set by wedgeWidth. This is a travelling wave retinotopy scan
- <b>contracting ring:</b>&nbsp;&nbsp;&nbsp;ring which contracts. Contraction speed is determined by the period (and eccentricity limits), drift speed (of the internal wedge bits) is set by animFreq (normally 0.2Hz), duty cycle (eccentricity width of ring) is set by dutyCycle. This is a travelling wave retinotopy scan
- <b>expanding ring:</b>&nbsp;&nbsp;&nbsp;ring which expands. Contraction speed is determined by the period (and eccentricity limits), drift speed (of the internal wedge bits) is set by animFreq (normally 0.2Hz), duty cycle (eccentricity width of ring) is set by dutyCycle. This is a travelling wave retinotopy scan
- <b>motionA:</b>&nbsp;&nbsp;&nbsp;motion localizer consisting of moving vs static dots. The first half of each period is moving dots, the second half is static dots. If preScanRest is ½ period, it will show static dots.
- <b>motionB:</b>&nbsp;&nbsp;&nbsp;&quot;inverse&quot; motion localizer consisting of moving vs static dots. The first half of each period is static dots, the second half is moving dots. If preScanRest is ½ period, it will show moving dots.
- <b>objectA:</b>&nbsp;&nbsp;&nbsp;object localizer consisting of intact vs. scrambled images. The first half of each period is intact images, the second half is scrambled images. If preScanRest is ½ period, it will show scrambled images
- <b>objectB:</b>&nbsp;&nbsp;&nbsp;&quot;inverse&quot; object localizer consisting of intact vs. scrambled images. The first half of each period is scrambled images, the second half is intact images. If preScanRest is ½ period, it will show intact images
- <b>full-field flickering checkerboard:</b>&nbsp;&nbsp;&nbsp;full field flickering checkerboard, on-off, with symmetric timing. Colors of the checkerboard and background can be specified, as can animation (flicker) frequency (animFreq). Number of wedges and width of wedge rings can be specified. Timing can be controlled by clocktime or scanner triggers:
   - <b>timebase=1:</b>&nbsp;&nbsp;&nbsp;(clock control) Stimulus is off for preScanRest time, on for period/2 time, and off for period/2 time.
   - <b>timebase=0:</b>&nbsp;&nbsp;&nbsp;(trigger control) Stimulus/rest is shown until N triggers are received. Stimulus is off for N=preScanRest/Tr, on for N=(1/2)*period/Tr, off for N=(1/2)*period/Tr
- <b>full-field flickering checkerboard asymmetric:</b>&nbsp;&nbsp;&nbsp;full field flickering checkerboard, on-off, with flexible timing. Stimulus is off for preScanRest time, on for stimDuration time, and off for (period - stimDuration) time.  Number of wedges and width of wedge rings can be specified. Colors of the checkerboard and background can be specified, as can animation (flicker) frequency
- <b>drifting checkerboard on-off:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), on-off  with symmetric timing. Stimulus is on for period/2 time and then off for period/2. Drift rate is controlled by animFreq
- <b>drifting checkerboard drift-static:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), drift vs. static with symmetric timing. Stimulus is drifting for period/2 time and then static for period/2. Drift rate is controlled by animFreq
- <b>drifting checkerboard center-surround:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), center vs. surround with symmetric timing. Stimulus is center for period/2 time and then the surround for period/2. Drift rate is controlled by animFreq. Center/surround cutoff radius is fixed at 4 degrees
- <b>drifting checkerboard center-inner-outer:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), center vs. inner surround vs. outer surround with symmetric timing. Stimulus is outer surround for preScanRest time, center for period/3 time, inner surround for period/3 time, and outer surround for period/2. Drift rate is controlled by animFreq. Center/inner surround border is given by Ralpha, inner surround/outersurround border is defined by Rbeta.
- <b>drifting checkerboard alternating halves:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), alternating halves  with symmetric timing. Stimulus is on the right side for period/2 time and then the left side for period/2. Drift rate is controlled by animFreq
- <b>drifting checkerboard on-off asymmetric:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), on-off  with asymmetric timing. Stimulus is on for stimDurationA time and then off for stimDurationB. Drift rate is controlled by animFreq
- <b>drifting checkerboard drift-static asymmetric:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), drift vs. static with asymmetric timing. Stimulus is  drifting for stimDurationA time and then static for stimDurationB. Drift rate is controlled by animFreq, number of AB repetitions per block is controlled by numReps, number of blocks is controlled by numBlocks, and inter-block rest is controlled by stimDurationRest
- <b>drifting checkerboard center-surround asymmetric:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), center vs. surround with asymmetric timing. Stimulus is center for stimDurationA time and then the surround for stimDurationB. Drift rate is controlled by animFreq. Center/surround cutoff radius is fixed at 4 degrees, number of AB repetitions per block is controlled by numReps, number of blocks is controlled by numBlocks, and inter-block rest is controlled by stimDurationRest
- <b>drifting checkerboard alternating halves asymmetric:</b>&nbsp;&nbsp;&nbsp;full field drifting checkerboard (black and white), alternating halves  with asymmetric timing. Stimulus is on the right side for stimDurationA time and then the left side for stimDurationB. Drift rate is controlled by animFreq, number of AB repetitions per block is controlled by numReps, number of blocks is controlled by numBlocks, and inter-block rest is controlled by stimDurationRest
- <b>VWFA localizer:</b>&nbsp;&nbsp;&nbsp;VWFA localizer using letters, non-letter symbols, and emoticons. Timing is hardcoded to present 12 trials per block and 3 blocks of each type, with 12s of rest in before starting, between blocks, and after the last block(restArestBrestCrestBrestArestCrestBrestCrestArest). Stimulus is presented for 0.75s with an ISI of 0.25s.
- <b>VWFA localizer images:</b>&nbsp;&nbsp;&nbsp;VWFA localizer using words and pictures of chairs, houses, and faces. Timing is hardcoded to present 10 trials per block and 4 blocks of each type, with 10s of rest in before starting, between blocks, and after the last block (restABCDrestBADCrestCBDArestDCABrest). Stimulus is presented for 0.75s with an ISI of 0.25s.

### List of Parameters
- <b>Tr</b> in seconds
- <b>preScanRest</b>   duration of ''rest'' to show before the stimulus starts. For retinotopy traveling waves (a,b), this will start the stimulus earlier in the period. For MT and LOC, this will start with the ''off'' condition. For checkerboard scans, this will show rest (blank gray screen with fixation). This time is not part of the number of full cycles
- <b>postScanRest</b>   duration of ''rest'' to show after the last stimulus ends. 
- <b>stimDuration</b> in seconds. Used for asymmetric flickering checkerboard scans
- <b>stimDurationA</b> in seconds. Used for asymmetric drifting checkerboard scans
- <b>stimDurationB</b> in seconds. Used for asymmetric drifting checkerboard scans
- <b>stimDurationRest</b> in seconds. Used for asymmetric drifting checkerboard scans
- <b>period</b>  in seconds (stimulus duration + rest, or full cycle for traveling waves)
- <b>numCycles</b>   how many full cycles of stimulus+rest or traveling waves to show. This doesn't include the preScanRest time
- <b>numReps</b> number of AB repetitions per block for asymmetric drifting checkerboard scans
- <b>numBlocks</b> number of (ABABrest) blocks for asymmetric drifting checkerboard scans
- <b>contrast</b>  0 to 1
- <b>innerRadius</b>   in degrees. The fixation mark size is fixed at 0.5*innerRadius, so innerRadius smaller than about 0.4 degrees could become too small to see.
- <b>outerRadius</b> in degrees. This can be as large as desired, but will be obviously be limited by the size of the screen
- <b>wedgeWidth</b> in degrees. The width of the rotating wedge
- <b>dutyCycle</b> in percent. The eccentricity width of the expanding/contracting ring, in percent (of outerRadius)
- <b>fixFraction</b>  the fraction of time (on average) that the fixation point could change. The task is for the subject to hit a button anytime the fixation mark (  +  ) rotates by 45 degrees (  x  ). The mark could change every 100 frames; this fraction determines whether or not it will.
- <b>animFreq</b> the flicker frequency in Hz for the flickering checkerboard, or the drift frequency for drifting checkerboards (normally 0.2Hz for retinotopic mapping)
- <b>colorA</b> first color of the checkerboard for flickering checkerboards only. Specify as an RGB triplet ranging from 0 to 1. E.g., [1,0,0] or [0.5,1,0]
- <b>colorB</b> second color of the flickering checkerboard, RGB triplet
- <b>colorBackground</b> background color for the flickering checkerboard, RGB triplet
- <b>monitor</b>  the ''monitor'' file (projector) to use. These will load up the linearized gamma table for that projector. This will populate a list of monitor files that have been created in monitor center on the local stimulus machines. At the CMRR, valid options are (depending on the scanner)
   - <b>7TASwest</b>
   - <b>7TASeast</b>
   - <b>7TPS</b>
   - <b>3TA</b>
   - <b>3TB</b>
   - <b>other</b>  loads up PsychoPy's ''testMonitor'', without gamma linearization
- <b>operatorScreen</b>   screen number for the operator, normally 0 for the primary display on the computer. Only used for flickering checkerboards, which display a graph of subject responses during the scan
- <b>subjectScreen</b>  screen number for the subject, normally 1 for the secondary display which is routed to the projector. If the two displays are mirrored, this should be 0 and the flickering checkerboards can't be run.
- <b>numScans</b>  the number of scans to be run. This number is used to initialize the variable containing the sequence of scans in the parameter file
- <b>timeBase</b>  whether the stimulus timing is controlled via computer's clock (1) or scanner triggers (0). Available only for flickering checkerboards with even timing (not for the asymmetric checkerboards)
- <b>Ralpha</b>  eccentricity border between center and inner surround for center/inner surround/outer surround drifting checkerboard, in degrees
- <b>Rbeta</b>  eccentricity border between inner surround and outer surround for center/inner surround/outer surround drifting checkerboard, in degrees
- <b>pairWedge</b> Option to display a pair of wedges (for improving fixation) in rotating wedge
- <b>fixationStyle</b> Option to have fixation mark change color (and rotate) for flickering checkerboard scans; 1 for rotation only, 2 for rotation and color change
- <b>trigger</b> allowed characters for trigger signal from scanner; defaults to <b>5t</b>
- <b>subject responses</b> allowed characters for subject responses; defaults to <b>1234bygr</b>
- <b>numWedgePairs</b> number of pairs of wedges in a flickering checkerboard               
- <b>ringWidth</b> width of each ring (in degrees of visual angle) for flickering checkerboards

## Instructions for running the code
- Launch the standalone PsychoPy application
- Open the file "retinotopy.py" located on the desktop in the folder pythonret
- Set up your parameter file, if desired (see full documentation or retinotopyParamsExample.py)
- Click the green run button or type CTRL-R (windows) or CMD-R (mac)
- Click on your desired running mode (parameter file or dynamic)
   - <b>parameter mode:</b>
      Choose the parameter file from the file-open dialog
   - <b>dynamic mode:</b>
      - Specify the general details for the scans.
      - Choose the stimulus type for the next scan.
      - Specify the specific parameters for that scan
      - When you are done, choose QUIT


## Detailed notes about parameters


|   |description |range [default] |wedge (cw or ccw) |ring (exp or cont) |motion (A or B) |object (A or B) |full field flickering checkerboard |full field flickering checkerboard with asymmetric timing |drifting checkerboard (on/off or drift/static or center-surround or alternating halves) |drifting checkerboard asymmetric (on/off or drift/static or center-surround or alternating halves) | drifting checkerboard center/inner/outer |VWFA localizer (images) |VWFA localizer (emoticons) |achromatic wedges (under development) |isoluminant checkerboards (under development) |
|---|------------|----------------|------------------|-------------------|----------------|----------------|-----------------------------------|----------------------------------------------------------|----------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|------------------------------------------|------------------------|---------------------------|--------------------------------------|----------------------------------------------|
|Tr |Tr in seconds |0.1 to infinity [2] |required |required |required |required |required |required |required |required | required |required |required | required |required  |
|innerRadius |inner radius in degrees |0 to infinity [0.5] |required |required |required |required |required |required | required |required |required |required |required | required |required  |
|fixFraction |fraction of the time the fixation task could happen |0 to 1 [0.2] |required |required |required |required |required | required |required |required |required |required |required | required |required  |
|monitor |monitor/projector |&nbsp; |required |required |required |required |required |required |required |required |required | required |required |required |required  |
|operatorScreen |which screen/desktop the operator sees |0 or 1 [0] |required |required |required |required |required |required |required |required |required |required |required | required |required  |
|subjectScreen |which screen/desktop the subject sees |0 or 1 [1] |required |required |required |required |required |required |required |required |required |required |required | required |required  |
|numScans |number of scans to run in a parameter file driven session |1 to infinity |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic |required in param file, N/A in dynamic  |
|preScanRest |rest condition before stimulus, or ''off condition'' stimulus |0 to infinity [12] |required |required |required |required | required |required |N/A |required |required |N/A |N/A |required |required  |
|postScanRest |rest condition after stimulus ends |0 to infinity [12] |N/A |required |required |required | required |required |N/A |required |required |N/A |N/A |required |required  |
|stimDuration |duration of stimulus in seconds |eps to infinity [0.75] |N/A |N/A |N/A |N/A |N/A |required |N/A |N/A | N/A |N/A |N/A |required |N/A  |
|stimDurationA |duration of stimulus A in seconds |eps to infinitiy [1] |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |required  |N/A  |N/A  |N/A  |N/A  |N/A  |
|stimDurationB  |duration of stimulus B in seconds  |eps to infinitiy [1]  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |required  |N/A  |N/A  |N/A  |N/A  |N/A  |
|stimDurationRest  |duration of inter-block rest in seconds  |eps to infinitiy [1]  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |required  |N/A  |N/A  |N/A  |N/A  |N/A  |
|period |period for traveling wave stimuli, or on+off time in others, in seconds |eps to infinity [24] |required |required |required |required |required |required |required | N/A |required |N/A |N/A |required | required  |
|numCycles |number of full cycles to display, in seconds |1 to infinity [10] |required |required |required |required |required | required |required | N/A |required |N/A |N/A |required |required  |
|numReps |number of AB repetitions per block |1 to infinity [5] |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |required  |N/A  |N/A  |N/A  |N/A  |N/A  |
|numBlocks |number of ABABrest blocks per scan |1 to infinity [10] |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |N/A  |required  |N/A  |N/A  |N/A  |N/A  |N/A  |
|contrast |stimulus contrast |0 to 1 [1] |required |required |required |N/A |N/A |N/A |required |required |required | N/A |N/A |N/A |N/A  |
|outerRadius |outer radius for wedges or dots |&gt;0.5 [12] |required |required |required (aperture for field of dots) |N/A |required |required |required |required |required |N/A |N/A |required |required  |
|wedgeWidth |width of wedges in rotating wedge, in degrees |0.36 to 360 degrees [45] |required |N/A |N/A |N/A |N/A |N/A | N/A | N/A |N/A |N/A |N/A |N/A |N/A  |
|dutyCycle |width of expanding/contracting ring, in percent |0 to 100 [25] |N/A |required |N/A |N/A |N/A |N/A |N/A | N/A | N/A |N/A |N/A |N/A |N/A  |
|animFreq |drifting or flickering frequency, in Hz |0 to infinity [0.2] |required |required |N/A |N/A |required |required | required |required |required |N/A |N/A |required | required  |
|colorA |first color for flickering checkerboards, as comma-separated RGB triplet |0 to 1 for each channel [1,0,0] |N/A |N/A |N/A |N/A | required |required |N/A | N/A |N/A |N/A |N/A |N/A |required  |
|colorB |second color for flickering checkerboards, as comma-separated RGB triplet |0 to 1 for each channel [1,0,0] |N/A |N/A |N/A |N/A | required |required |N/A | N/A |N/A |N/A |N/A |N/A |required  |
|colorBackground |background color for flickering checkerboards, as comma-separated RGB triplet |0 to 1 for each channel [1,0,0] |N/A |N/A |N/A | N/A |required |required |N/A | N/A |N/A |N/A |N/A |required |required  |
|timeBase |whether timing is advanced by clock time or triggers, for flickering checkerboards |1 (time based) or 0 (trigger based) [1] |N/A |N/A |N/A |N/A |required |N/A |N/A | N/A |N/A |N/A |N/A |N/A |required  |
|fixationStyle |whether fixation mark only rotates (1) or rotates and changes color (2) |1 or 2 |N/A |N/A |N/A |N/A | required |required |N/A | N/A |N/A |N/A |N/A |N/A |required  |
|Ralpha |eccentricity border between center and inner surround for center/inner surround/outer surround drifting checkerboard, in degrees |&lt;Rbeta [1.0] |N/A | N/A |N/A |N/A |N/A |N/A |N/A | N/A |required |N/A |N/A |N/A |N/A  |
|Rbeta |eccentricity border between inner and outer surrounds for center/inner surround/outer surround drifting checkerboard, in degrees |Ralpha&lt;Rbeta&lt;outerRadius [2.0] |N/A |N/A |N/A |N/A |N/A |N/A |N/A | N/A |required |N/A |N/A |N/A |N/A  |
|pairWedge |whether a second wedge is drawn at 180 degrees from the first wedge for rotating wedge scans  |0 (no) or 1 (yes) [0] |required |N/A |N/A |N/A |N/A |N/A |N/A | N/A |N/A |N/A |N/A |N/A |N/A  |
|numWedgePairs |number of wedge pairs |1 to anything [8] |N/A |N/A |N/A |N/A | required |required |N/A | N/A |N/A |N/A |N/A |N/A |required  |
|ringWidth |width of rings (degrees of visual angle) |anything [1.0] |N/A |N/A |N/A |N/A | required |required |N/A | N/A |N/A |N/A |N/A |N/A |required  |
