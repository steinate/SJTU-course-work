import numpy as np
import cv2
import random

img=cv2.imread("tj.jpg")
imgold=img.copy()
point=0

def hitmouse(event,x,y,flags,param):
    global i,j,point
    if event==cv2.EVENT_LBUTTONDOWN and i*100<=x<=(i+1)*100 and j*100<=y<=(j+1)*100:
        point=point+100
        print(point)

while True:
    img=imgold.copy()
    cv2.namedWindow('Tom')
    head=img[230:330,600:700].copy()
    i=random.randint(0,2)
    j=random.randint(0,2)
    img[i*100:(i+1)*100,j*100:(j+1)*100]=head

    for m in range(3):
        for k in range(3):
            cv2.rectangle(img,(m*100,k*100),((m+1)*100,(k+1)*100),(0,255,0),5)

    cv2.imshow('Tom',img)
    for n in range(10):
        cv2.setMouseCallback('Tom',hitmouse)
        cv2.waitKey(10)
    
