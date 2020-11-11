import cv2
import numpy as np

cap=cv2.VideoCapture(0)

trackx=[]
tracky=[]

while True:
    ret,img=cap.read()
    img=cv2.flip(img,1)
    
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green=np.array([35,43,46])
    upper_green=np.array([77,255,255])
    redobj=cv2.inRange(imghsv,lower_green,upper_green)
    conts,hrc=cv2.findContours(redobj,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    bigconts=[]
    for cont in conts:
        area=cv2.contourArea(cont)
        if area>400:
            bigconts.append(cont)

    for bigcnt in bigconts:
        M=cv2.moments(bigcnt)
        cx=int(M['m10']/M['m00'])
        cy=int(M['m01']/M['m00'])
        trackx.append(cx)
        tracky.append(cy)
        
    for i in range(len(trackx)):
        cv2.circle(img,(trackx[i],tracky[i]),1,(0,0,255),5)

    cv2.imshow("img",img)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
