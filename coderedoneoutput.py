# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:32:29 2022

@author: SpencerW
"""

import cv2
import cv2 as cv
import imutils
import numpy as np
import time
cap = cv2.VideoCapture(0)
fileout=open('80cm.txt','w')
# The device number might be 0 or 1 depending on the device and the webcam

while(True):
    _, frame = cap.read()
    centers=[]
    height =[]
    hsv_frame =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    light_orange = (94, 188, 92) # previous value 1,190, 200
    dark_orange  = (125, 240, 255) 
    mask = cv2.inRange(hsv_frame, light_orange, dark_orange)
    color_segmented = cv2.bitwise_and(frame, frame, mask=mask)
    
    color = (0, 0, 255)
    imgray = cv.cvtColor(color_segmented, cv.COLOR_BGR2GRAY)
   # #edged = cv2.Canny(imgray, 50, 100)
    ##edged = cv2.dilate(edged, None, iterations=1)
    ##edged = cv2.erode(edged, None, iterations=1)
    edged = imgray 
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(frame, contours, -1, (0,255,0), 2)
    
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
            
        
        
        x,y,w,h = cv2.boundingRect(c)
        height.append(h)
        if len(height) >=2:
            print(height[0], height[1])
        cv2.putText(frame, str(h), (x,y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 1)
        fileout.write(str(h))
        fileout.write('\t')
        fileout.write('\n') 
        
        
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append([cX,cY])
	# draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            x = cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            h, w = edged.shape
           # print(h,'      ',w)
           


            if len(centers) >=2:
                dx= centers[0][0] - centers[1][0]
                dy = centers[0][1] - centers[1][1]
                D = np.sqrt(dx*dx+dy*dy)
                #print(D)
                #cv2.line(frame, (centers[0][0], centers[0][1]), (centers[1][0], centers[1][1]), (0, 255, 0), 2)
                Dist = str(D)
                fileout.write(Dist)
                
                #cv2.putText(frame, Dist, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
            
            
            
                
            

            
            
        else:
    
     
    
            #cv2.imshow('edged', edged)
            #cv2.imshow('graythresh', imgray)
            cv2.imshow('frame', frame)
            cv2.imshow('frame1', color_segmented)
            cv2.imshow('frame2', edged)
            #cv2.imshow('colormask', color_segmented)
           
    if cv2.waitKey(1) & 0xFF == ord('q'):
        
        break
fileout.close()    
cap.release()
cv2.destroyAllWindows()