# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import shutil

faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("trainer\\trainingData.yml")
id=0
name="NONE"
font=cv2.FONT_HERSHEY_COMPLEX_SMALL

X_data = []
files = glob.glob ("img/*.jpg")
for myFile in files:
    image = cv2.imread (myFile)
##    X_data.append (image)

    ret, img = True, image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        print(id)
        if conf < 60:
            if id==1:
                name="Found"
               
                shutil.copy(myFile, "img_results/")
            else:
                name="NOONE"
                print(myFile + "   NONE")
        #cv2.putText(img,name,(x,y+h),font,6,(0,0,255),4)
    
    #cv2.imshow("Face",img)
    if(cv2.waitKey(1)==ord('q')):
        break

    
cam.release()
cv2.destroyAllWindows()
    
