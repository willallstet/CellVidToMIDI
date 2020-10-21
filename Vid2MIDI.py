import numpy as np
import cv2
from midiutil import MIDIFile

#video file
fileName="009_000_0 (RbcL_GFP_145hrs_25redLIDA_lightgradient_0000).mov"
vidObj = cv2.VideoCapture(fileName)#open video
fps=30 #video frames per second
freq=0.5 #how often contours are checked (in seconds)
# Used as counter variable
count = 0
count2 = 0
# checks whether frames were extracted
success = 1
#array to hold sizes and times of contours later
contour_areas=[]
MyMIDI = MIDIFile(1)  # midi file we output to
MyMIDI.addTempo(0, 0, 60) #made at 60BPM so each second is a note
while success:
    success, image = vidObj.read() #open current frame
    if count%(fps*freq)==0: #does it once every 30 frames
        analyze=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#converts to grey and ups contrast + brightness
        ret, thresh = cv2.threshold(analyze, 30, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image, contours, -1, (0,255,0), 3)
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 600,600)
        cv2.imshow('frame',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #all the notes in the key of C
        acceptableNotes=[83,81,79,77,76,74,72,71,69,67,65,64,62,60,59,57,55,53,52,50,48,47,45,43,41,40,38,36,35,33,31,29,28,26,24]
        #for each contour add it to the list
        for i in contours:
            contour_areas.append([cv2.contourArea(i),count/(fps*freq)])
        contour_areas.sort(reverse=False,key=lambda x: x[0]) #put them in order
    count += 1 #count that frame as read
for i in range(len(contour_areas)):#for loop to add all the contours to the midi file
    MyMIDI.addNote(0,0,acceptableNotes[count2],contour_areas[i][1],1,100)
    if(i%(int(len(contour_areas)/28))==0 and i!=0):#if that note is full
        count2+=1;#move to the next one
vidObj.release()#close video
with open(fileName+"_sound.mid", 'wb') as output_file:#save the midi file
    MyMIDI.writeFile(output_file)
