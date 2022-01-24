import cv2
import numpy as np
import sys
import torch

cap=cv2.VideoCapture(0)
width = 640
hight = 480
ret = cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
ret = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hight)
max_length = 512
trackx=[]
tracky=[]
WHITE_RGB = (255, 255, 255)
CLASSES = ["apple", "book", "bowtie", "candle", "cloud", "cup", "door", "envelope", "eyeglasses", "guitar", "hammer",
           "hat", "ice cream", "leaf", "scissors", "star", "t-shirt", "pants", "lightning", "tree"]

if torch.cuda.is_available():
    model = torch.load("trained_models/whole_model_quickdraw")
else:
    model = torch.load("trained_models/whole_model_quickdraw", map_location=lambda storage, loc: storage)
model.eval()

while True:
    ret,img=cap.read()
    img=cv2.flip(img,1)
    canvas = np.zeros((480, 640, 3), dtype=np.uint8)
    
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green=np.array([100,43,46])
    upper_green=np.array([124,255,255])
    # lower_green=np.array([156,43,46])
    # upper_green=np.array([180,255,255])
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
        if 0<cx<80 and 0<cy<80:
            trackx=[]
            tracky=[]
            break
        if 560<cx<640 and 0<cy<80:
            sys.exit()
        trackx.append(cx)
        tracky.append(cy)
    if len(trackx) != 0:
        ix, iy = trackx[0],tracky[0]
        for i in range(len(trackx)):
            cv2.line(img, (ix, iy), (trackx[i],tracky[i]), (255, 255, 0), 5)
            cv2.line(canvas, (ix, iy), (trackx[i],tracky[i]), (255, 255, 0), 5)
            ix, iy = trackx[i],tracky[i]
        
    cv2.rectangle(img, (560, 0), (640, 80), (0, 255, 0), 2)    
    cv2.rectangle(img, (0, 0), (80, 80), (0, 255, 0), 2) 
    cv2.rectangle(img, (0, 400), (80, 480), (0, 255, 0), 2) 

    cv2.imshow("img",img)
    # cv2.imshow("canvas",255 - canvas)
    key=cv2.waitKey(5)
    if key==ord('q'):
        break
    elif key==ord(' '):
        print('judging.............')
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        ys, xs = np.nonzero(canvas)
        # print(ys, xs)
        min_y = np.min(ys)
        max_y = np.max(ys)
        min_x = np.min(xs)
        max_x = np.max(xs)
        canvas = canvas[min_y:max_y, min_x: max_x]

        canvas = cv2.resize(canvas, (28, 28))
        canvas = np.array(canvas, dtype=np.float32)[None, None, :, :]
        canvas = torch.from_numpy(canvas)
        logits = model(canvas.cuda())
        print(CLASSES[torch.argmax(logits[0])])
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        trackx=[]
        tracky=[]
        # trackx=[0]*max_length
        # tracky=[0]*max_length

cv2.destroyAllWindows()
cap.release()
