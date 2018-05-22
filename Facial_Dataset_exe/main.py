import kivy
kivy.require('1.0.6')

from glob import glob
from random import randint
import os
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
import cv2

class pop(Widget):

    
    
    def remove_img(self, path):
        os.remove(path)
        
        
    
    
        
    
    def show_it(self,Picture):
        pic = Picture
        def delete_pic(self):
            print("hoi")
            pic._set_x(-1000)
            pic._set_y(-1000)
            
            
            
        
        self.box=FloatLayout()
        
        self.lab=(Label(text="Are you sure you do not want this picture? ",font_size=15,
        	size_hint=(None,None),pos_hint={'x':.25,'y':.6}))
        self.box.add_widget(self.lab)
        
        self.but=(Button(text="close",size_hint=(None,None),
        	width=200,height=50,pos_hint={'x':0,'y':0}))
        self.box.add_widget(self.but)

        self.delet=(Button(text="Delete",size_hint=(None,None),
        	width=200,height=50,pos_hint={'x':.5,'y':0}))
        self.box.add_widget(self.delet)
       
        self.main_pop = Popup(title="Warning",content=self.box,
        	size_hint=(None,None),size=(450,300),auto_dismiss=False,title_size=15)
        
        self.but.bind(on_press=self.main_pop.dismiss)

        self.delet.bind(on_press=delete_pic)

        self.main_pop.open()
        
        


class remove_place(Scatter):
    
    source = StringProperty(None)
    
class Picture(Scatter, ButtonBehavior):

    def on_press(self):
       print("UP")
            
    
    source = StringProperty(None)


class PicturesApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root
        
        def delete_camera():
            root.remove_widget(self.my_camera)
            #self.capture.release()
            
            
        def build_camera():
            def start_button(self):
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
                            cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

                        #cv2.imshow('Face',img)
                        #wait for 100 miliseconds
                            
                        if cv2.waitKey(100) & 0xFF == ord('q'):
                           
                            break
                        # break if the sample number is morethan 20
                        elif sampleNum>20:
                            
                            break
                    
                    
                    delete_camera()
                    
                    os.system("trainner 1")
                    os.system("detector_img 1")
                    root.remove_widget(start)
                    
                    build_picturescreen()
                create_dataset()

            cap = cv2.VideoCapture(0)
            self.capture = cap
            self.my_camera = KivyCamera(capture=self.capture, fps=60)
            start = Button(text="Scan your face", size=(3,3), size_hint=(0.15,0.1),pos_hint={'center_x': 0.5, 'center_y': 0.1} )
            start.bind(on_press=start_button)
            root.add_widget(start)
            root.add_widget(self.my_camera)

        def build_picturescreen():
        
            root.add_widget(Label(text="Pictures",  font_size='80sp', size_hint=(0.23, 0.2)))
            root.add_widget(Button(text='Buy', pos_hint={'x': 0.8, 'y': 0.05}, size_hint=(0.15,0.1)))
            layout = ScrollView(size_hint=(None, None), size=(800, 820), pos_hint={'center_x': 0.5, 'center_y': .525}, do_scroll_x=False)
            #layout.bind(minimum_height=layout.setter('height'))
            
            

            box = GridLayout(cols=4, size_hint_y=None)
            box.bind(minimum_height=box.setter("height"))
            5
            layout.add_widget(box)

            root.add_widget(layout)
            img = Picture(source="remove.png", rotation=randint(0, 0), pos=(1430, 760))
            
            
            root.add_widget(img)

            
            
            # get any files into images directory
            curdir = dirname(__file__)
            counter = 100
            counter2 = 100
            print("test0")
            def picture_press(instance):
                print("hey")
            for filename in glob(join(curdir, 'img_results', '*')):
                print("test")
                try:
                    # load the image
                    picture = Picture(source=filename, rotation=randint(0, 0), pos=(counter2,counter))
                    
                    picture.bind(on_press=picture_press)
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
        build_camera()
        #-------
                    
    def on_pause(self):
        return True
    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()

    
class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        updates = Clock.schedule_interval(self.update, 1.0 / fps)


    
    def update(self, dt):
        
        
        face_cascade = cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('hc/haarcascade_eye.xml')
        ret, frame = self.capture.read()
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
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
    
