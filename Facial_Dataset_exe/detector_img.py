# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import shutil
import time

def recog(save):
	#Variable: the parameter of CascadeClassifier is the xml used to detect faces
    faceDetect=cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')

    
    
    cam=cv2.VideoCapture(0)
    rec=cv2.face.LBPHFaceRecognizer_create()
	#Variable: the parameter of read is the file with data created in the training phase
    rec.read("trainer\\trainingData.yml")
    id=0
    name="NONE"
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL

    X_data = []
    ImageList = []
    bestImage = None
    bestImageValue = None
	#Variable: the parameter of glob is the map and file type it will put in the files collection
    files = glob.glob ("img/*.jpg")
    lowest_conf = 200
    for myFile in files:
        start = time.time()
        print("--------------------------------------------")
        print("Scanning: " + myFile)
        reco = False
        det = False
        
        image = cv2.imread (myFile)

        ret, img = True, image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		#Variable: parameters of detectMultiScale, gray is the image, scaleFactor and minNeighbors
        faces=faceDetect.detectMultiScale(gray, 1.2, 10)

        for (x,y,w,h) in faces:
            det = True
            id,conf=rec.predict(gray[y:y+h,x:x+w])
            print('Prediction: ' + str(conf))
            if conf < lowest_conf:
                lowest_conf = conf
                bestImage = myFile
                bestImageValue = [x, y, w, h]
                print(bestImage + "-------------------------------------------------------------BEST IMAGE")
			#Variable: if conf is lower than, here you can adjust the confidence needed to become a match
            if conf < 36:
                if id==1:
					#Variable: if conf is lower than, these images will always be added to the dataset for recursion
                    if conf < 0:
                        ImageList.append(myFile)

                    reco = True
                    name = "Found"
                    if save:
						#Variable: the second parameter of the copy method, this is the directory the matches will be copied to
                        shutil.copy(myFile, "img_results/")

                        

                else:
                    name="NOONE"
                    
        
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
    ImageList.append(bestImage)

    cam.release()
    cv2.destroyAllWindows()
    return {'image':ImageList, 'values':bestImageValue}


        
