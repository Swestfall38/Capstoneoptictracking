import cv2
import cv2 as cv
import imutils
import numpy as np
cap = cv2.VideoCapture()
# The device number might be 0 or 1 depending on the device and the webcam
cap.open(0, cv2.CAP_DSHOW)
while(True):
    _, frame = cap.read()
    centers=[]
    hsv_frame =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    light_orange = (41,15,0) # previous value 1,190, 200
    dark_orange  = (92,246,246) 
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
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centers.append([cX,cY])
	# draw the contour and center of the shape on the image
            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
            x = cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)


            if len(centers) >=2:
                dx= centers[0][0] - centers[1][0]
                dy = centers[0][1] - centers[1][1]
                D = np.sqrt(dx*dx+dy*dy)
                #print(D)
                cv2.line(frame, (centers[0][0], centers[0][1]), (centers[1][0], centers[1][1]), (0, 255, 0), 2)
                Dist = str(D)
                cv2.putText(frame, Dist, (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            
            
            
            
            

            
            
        else:
    
    
    
            #cv2.imshow('edged', edged)
            #cv2.imshow('graythresh', imgray)
            cv2.imshow('frame', frame)
            cv2.imshow('frame1', color_segmented)
            #cv2.imshow('colormask', color_segmented)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
