import cv2 as cv
import datetime
import numpy as np
import time
import mouse as m
import time
import HandTrackingModule as htm
import pyautogui as pg
import pydirectinput as pn
import win32api, win32con



wCam,hCam = 1280,720
plocx,plocy=0,0
clocx,clocy=0,0

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
tipIds = [4,8,12,16,20]
last_click = datetime.datetime.now()
detector = htm.HandDetector(maxHands=1,detectionCon=0.75)

while True:
    success,img = cap.read()
    img = cv.flip(img,1)
    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    

    lower_red = np.array([0,139,184])
    upper_red = np.array([179,255,255])
    mask_red = cv.inRange(hsv, lower_red, upper_red)

    
    contoursRed, _ = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for c in contoursRed:
        if cv.contourArea(c)<=50:
            continue

        x, y, _, _ = cv.boundingRect(c)
        

            
        clocx = plocx + (x-plocx)/6 
        clocy = plocy + (y-plocy)/6

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(clocx-plocx), int(clocy-plocy), 0, 0)
            
        
        plocx,plocy = clocx,clocy
        cv.drawContours(img, contoursRed, -1, (0, 255, 0), 3)


   

    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList)!=0:
        #x1,y1=lmList[8][1:]

        fingers = []

        #THUMB
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #FINGERS
        for id in range(1,5):

            if lmList[tipIds[id]][2] < lmList[tipIds[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        
        if fingers[1]==1:
            pn.keyDown('w')
        else:
            pn.keyUp('w')

        if fingers[0]==1:
            m.press()
        else:
            m.release()
    
    
    cv.imshow("Image",img)

    key = cv.waitKey(1)
    if key==27:
        break;

    
    

    

cap.release()