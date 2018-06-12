import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
import os
import sys
from kivy.uix.label import Label
from os.path import join, dirname
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from time import sleep
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
import glob as globs
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from subprocess import Popen, PIPE
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
import threading
from subprocess import call
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen
import importlib
import cv2
from kivy.graphics import Line, Color
import trainner
from kivy.animation import Animation
from kivy.clock import mainthread
import detector_img
import time
import threading

class remove_place(Scatter):
    
    source = StringProperty(None)

class Picture(Scatter):

    def on_touch_down(self, touch):
       
        print(touch.x)
        print(touch.y)
        
        return True

    
    source = StringProperty(None)

class ConvertBlack():
    def ConvertImages():
        
        files = globs.glob ("img/*.jpg")
        for myFile in files:
                
            print(myFile)
            img = cv2.imread(str(myFile))
            myFile = myFile[4:-4]
            img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
            cv2.imwrite("img/Black/" + myFile + ".jpg", img)
         
            print("Write Completed")
              
        
           
class PicturesApp(App):

    
    def build(self):

        # the root is created in pictures.kv
        root = self.root
        
        
        def delete_camera():
            root.remove_widget(self.my_camera)
            
            
        
            
        
        def build_camera():

            picture_text = Label(text="Look at the camera",  font_size='80sp', size_hint=(1, 1.8))
            root.add_widget(picture_text)
           
            
            def start_button(self):

                loading_pic = Picture(source='Assets/loading.gif', pos=(self.parent.width /2 - self.width /2, 400))
                @mainthread
                def create_loading_gif():
                    
                    root.add_widget(loading_pic)
                                                  
                @mainthread
                def delete_loading_gif():
                    root.remove_widget(loading_pic)
                    
                                 
                def create_dataset():

                    
                    
                     
                    path2 = r'img_results'
                    for file in os.listdir('img_results'):
                        if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png'):
                            os.remove(path2+ "/" + file) 

                    path = r'dataSet'
                    for file in os.listdir('dataSet'):
                        if file.endswith('.jpg'):
                                os.remove(path+ "/" + file)
                                
                    cam = cap
                    detector=cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')
                    Id = "1"
                    sampleNum=0
                    
                    
                    
                    while(True):
                        
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = detector.detectMultiScale(gray, 1.3, 5)
                        
                        for (x,y,w,h) in faces:
                            
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                            #incrementing sample number 
                            sampleNum=sampleNum+1
                            #saving the captured face in the dataset folder
                            fotoSource = "dataSet/User."+Id +'.'+ str(sampleNum) 
                            cv2.imwrite(fotoSource + ".jpg", gray[y:y+h,x:x+w])

                            #create mirror image
                            dsFoto = cv2.imread(fotoSource + ".jpg")
                            vertical_img = dsFoto.copy()
                            vertical_img = cv2.flip(dsFoto, 1)
                            cv2.imwrite(fotoSource + "mirror" + ".jpg", vertical_img)
                            

                        #cv2.imshow('Face',img)
                        #wait for 100 miliseconds
                            
                        if cv2.waitKey(1000) & 0xFF == ord('q'):
                           
                            break
                        # break if the sample number is morethan ...
                        elif sampleNum>15:
                            
                            break
                    
                    
                    
                    delete_camera()
                    create_loading_gif()
                    root.remove_widget(picture_text)
                    
                    trainner.train()
                    
                    KivyCamera.CancelUpdate()
                    
                    detector_img.recog()
                    
                    
                    root.remove_widget(start)

                    delete_loading_gif()
                    
                    build_picturescreen()

          
                t = threading.Thread(target=create_dataset)
                t.start()

                
                
                
                
            cap = cv2.VideoCapture(0)
            self.capture = cap
            self.my_camera = KivyCamera(capture=self.capture, fps=60)
            start = Button(text="Scan your face", size=(3,3), size_hint=(0.15,0.1),pos_hint={'center_x': 0.5, 'center_y': 0.1} )
            start.bind(on_press=start_button)
            root.add_widget(start)
            root.add_widget(self.my_camera)
        @mainthread
        def build_picturescreen():

            
            
            def exit_session(self):
                build_camera()
                root.remove_widget(layout)
                root.remove_widget(picture_text)
                root.remove_widget(exit_button)
                root.remove_widget(buy_button)

    

            picture_text = Label(text="Pictures",  font_size='80sp', size_hint=(0.23, 1.8))
            root.add_widget(picture_text)
            
            
            buy_button = Button(text='Buy', pos_hint={'x': 0.82, 'y': 0.05}, size_hint=(0.15,0.1))
            root.add_widget(buy_button)
            exit_button = Button(text='Exit', pos_hint={'x': 0.03, 'y': 0.05}, size_hint=(0.15,0.1))
            exit_button.bind(on_press=exit_session)
            root.add_widget(exit_button)
            layout = ScrollView(size_hint=(None, None), size=(930, 630), pos_hint={'center_x': 0.5, 'center_y': .525}, do_scroll_x=False)
            #layout.bind(minimum_height=layout.setter('height'))
            
            

            box = GridLayout(cols=3, size_hint_y=None)
            box.bind(minimum_height=box.setter("height"))
            
            layout.add_widget(box)

            root.add_widget(layout)
            
            
            # get any files into images directory
            curdir = dirname(__file__)
            counter = 100
            counter2 = 100
            
            
            

            
            for filename in glob(join(curdir, 'img_results', '*')):
                
                
                try:
                    # load the image
                    
                     
                    picture = Picture(source=filename, rotation=randint(0, 0), pos=(counter2,counter))
                    
                    counter = counter + 150
                    if counter > 700:
                        counter = 100
                        counter2 = counter2 + 150
                
                    #picture.on_touch_down: print("hey")
                
            
                    # add to the main field
                  
                    box.add_widget(picture)
                 
                except Exception as e:
                    Logger.exception('Pictures: Unable to load <%s>' % filename)        
        #Start here your methods
        #build_camera()
        build_picturescreen()
        #ConvertBlack.ConvertImages()
        #-------
                    
    def on_pause(self):
        return True
    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()

    
class KivyCamera(Image):

    
    def __init__(self, capture, fps, **kwargs):
        global updates
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        updates = Clock.schedule_interval(self.update, 1.0 / fps)


    def CancelUpdate():
        global updates
        updates.cancel()
    
    def update(self, dt):
        
        
        face_cascade = cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('hc/haarcascade_eye.xml')
        ret, frame = self.capture.read()
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.05, 3)
        
        # Display the resulting frame
        
        for (x,y,w,h) in faces:
             cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
             roi_gray = gray[y:y+h, x:x+w]
             roi_color = frame[y:y+h, x:x+w]
             eyes = eye_cascade.detectMultiScale(roi_gray)
             for (ex,ey,ew,eh) in eyes:
                 cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
    
            



if __name__ == '__main__':
    Window.size = (1920, 1080)
    Window.fullscreen = "auto"
    PicturesApp().run()
    
