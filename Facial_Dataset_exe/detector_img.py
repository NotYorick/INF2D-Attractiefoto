# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import shutil
import time

def recog():
    faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam=cv2.VideoCapture(0)
    rec=cv2.face.LBPHFaceRecognizer_create()
    rec.read("trainer\\trainingData.yml")
    id=0
    name="NONE"
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL

    X_data = []
    #files = glob.glob ("img/Black/*.jpg")
    files = glob.glob ("img/*.jpg")
    for myFile in files:
        start = time.time()
        print("--------------------------------------------")
        print("Scanning: " + myFile)
        reco = False
        det = False
        
        image = cv2.imread (myFile)
    ##    X_data.append (image)

        ret, img = True, image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces=faceDetect.detectMultiScale(gray, 1.1, 5)
        for (x,y,w,h) in faces:
            det = True
            #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            print('Prediction: ' + str(conf))
            if conf < 60:
                if id==1:
                    reco = True
                    name="Found"
                    
                    shutil.copy(myFile, "img_results/")
                else:
                    name="NOONE"
                    
            #cv2.putText(img,name,(x,y+h),font,6,(0,0,255),4)
        
        #cv2.imshow("Face",img)
        if(cv2.waitKey(1)==ord('q')):
            break
        if reco:
            print("RECOGNIZED")
        else:
            print("NOT RECOGNIZED")
        if det:
            print("DETECTED")
        else:
            print("NOT DETECTED")
        end = time.time()
        print(end - start)

        
    cam.release()
    cv2.destroyAllWindows()
        
