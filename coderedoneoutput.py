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

# -10 for lit-room, -4 for dark room 
cap.set(cv2.CAP_PROP_EXPOSURE, -10)
#time.sleep(100)
while(True):
    _, frame = cap.read()
    gapmat1=[]
    gap=0
    gap2 = 0
    gapmat2=[]
    bigvec=0
    centers=[]
    gapmat=[]
    height =[]
    width =[]
    hsv_frame =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    daylowb_green = (56, 132, 42)
    dayupb_green  = (76, 227, 255) 
    nightlowb_green = (64, 11, 70)
    nightupb_green = (112,206,255)
    #daylowb_green = (55, 30, 81)# previous value 1,190, 200
   # dayupb_green  = (91,255,255) 
   # nightlowb_green = (64, 11, 70)
   # nightupb_green = (112,206,255)
    
    #get avg intensity
    avg_intensity = np.mean(cv.cvtColor(frame,cv.COLOR_BGR2GRAY))
    #print('intensity:',avg_intensity)
  
    
    
    #if (avg_intensity > 50):
    mask = cv2.inRange(hsv_frame, daylowb_green, dayupb_green)
    #else:
        # set for night  
       ## mask = cv2.inRange(hsv_frame, nightlowb_green, nightupb_green)
    
    
    color_segmented = cv2.bitwise_and(frame, frame, mask=mask)
    
    color = (0, 0, 255)
    imgray = cv.cvtColor(color_segmented, cv.COLOR_BGR2GRAY)
    #edged = cv2.Canny(imgray, 50, 100)
    
    ##edged = cv2.erode(edged, None, iterations=1)
    #imgray = cv2.medianBlur(imgray, 3)
    se = np.ones((5,5),dtype='uint8')
    edged = cv2.morphologyEx(imgray, cv2.MORPH_CLOSE, se)
    cnts = cv2.findContours(imgray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(frame, contours, -1, (0,255,0), 2)
    
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
     
        
        # if smaller than 20 pixles, ignore
        n_pixels = np.count_nonzero(c)
        if n_pixels < 40:
            continue
            
        
        x,y,w,h = cv2.boundingRect(c)
        if h>100:
            height.append(h)
        if w>100:    
            width.append(w)
        if len(height) >=2:
            fileout.write('Heights: ')
            fileout.write(str(height[0]))
            fileout.write('\t')
            fileout.write(str(height[1]))
            fileout.write('\n') 
        
            
        if len(height)>=2:
            gap = abs(height[0]-height[1])
            
          
        gapmat1.append(gap)
       # for i in gapmat1:  
            #print(i,'\t',i-1)
            
        
            
        
        
        #(gapmat)   

  
            #if :
               # print('move right')
           # if height[1]>height[0]:  
                #print('move left')
                

        if len(width) >=2:
            fileout.write('WIDTHS: ')
            fileout.write(str(width[0]))
            fileout.write('\t')
            fileout.write(str(width[1]))
            fileout.write('\n') 
        if len(width)>=2:
            gap2 = abs(width[0]-width[1])
            
          
        gapmat2.append(gap2)
        for x in gapmat2:  
            print('width  ',x,'\t',x-1)
            
            
            
            
        if h > 100:    
            cv2.putText(frame, str(h), (x+25,y + 100), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        if w > 100:    
            cv2.putText(frame, str(w), (x+100,y +50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (60,20,220), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 1)


        
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
                #fileout.write(Dist)
                
                #cv2.putText(frame, Dist, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
        
 
          
    #cv2.imshow('edged', edged)
    #cv2.imshow('graythresh', imgray)
    cv2.imshow('frame', frame)
    cv2.imshow('frame1', color_segmented)
    #cv2.imshow('frame2', edged)
    #cv2.imshow('colormask', color_segmented)
    
    if cv2.waitKey(100) & 0xFF == ord('q'):
        
        
        
        
        break
    

fileout.close()    
cap.release()
cv2.destroyAllWindows()