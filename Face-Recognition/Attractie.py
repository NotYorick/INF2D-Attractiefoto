# verwijderen dataset
# nieuwe dataset  id = 1
# trainer
# detector image
# return image

#files = glob.glob ("dataSet/*.jpg")

import os

#path2 = r'C:\Users\DaanS\Desktop\Face-Recognition-master\img_results'

path2 = r'img_results'
for file in os.listdir('img_results'):
    if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png'):
        os.remove(path2+ "/" + file) 

path = r'dataSet'
for file in os.listdir('dataSet'):
    if file.endswith('.jpg'):
        os.remove(path+ "/" + file) 

print("Kijk in de camera!!!")
print("Creating dataset...")
os.system("datasetCreator.py 1")
print("Making trainer from photos")
os.system("trainner 1")
print("Detecting faces")
os.system("detector_img 1")

