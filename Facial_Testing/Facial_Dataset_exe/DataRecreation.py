import cv2,os
import numpy as np
from PIL import Image


def Recreate(self, imagelist):
    ImageList = imagelist['image']
    bestImageValues = imagelist['values']
    detector = cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')
    Id = "1"
    sampleNum = 16

    for file in ImageList:

        file = cv2.imread(file)
        ret, img = True, file
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            x = bestImageValues[0]
            y = bestImageValues[1]
            w = bestImageValues[2]
            h = bestImageValues[3]

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # incrementing sample number
            sampleNum = sampleNum + 1
            # saving the captured face in the dataset folder
            cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

        # cv2.imshow('Face',img)
        # wait for 100 miliseconds

        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
            # break if the sample number is morethan ...




