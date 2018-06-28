import kivy
import os
import glob as globs
import cv2
import trainner
import detector_img
import threading
import DataRecreation
import shutil

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from win32api import GetSystemMetrics
from kivy.animation import Animation
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import FocusBehavior
from kivy.clock import Clock
from kivy.uix.behaviors.compoundselection import CompoundSelectionBehavior
from kivy.graphics.texture import Texture
from kivy.clock import mainthread

kivy.require('1.0.6')


class remove_place(Scatter):
    source = StringProperty(None)


class Picture(Scatter, GridLayout, CompoundSelectionBehavior, FocusBehavior):
    selected = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print (os.path.basename(self.source))
            print ("selected before =", self.selected)
            if self.selected == False:
                shutil.copy(self.source, 'selected/')
                self.selected = True
                print ("selected after =", self.selected)
            elif self.selected == True:
                os.remove('selected/' + os.path.basename(self.source))
                self.selected = False
                print ("selected after =", self.selected)
        return

    def checkselected():
        return self.selected

    source = StringProperty(None)
    


class ConvertBlack():

    def ConvertImages(self):
        files = globs.glob ("img/*.jpg")
        for myFile in files:
            print(myFile)
            img = cv2.imread(str(myFile))
            myFile = myFile[4:-4]
            img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY )
            cv2.imwrite("img/Black/" + myFile + ".jpg", img)
            print("Write Completed")


class PicturesApp(App):

    def animate(self, instance):

        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        animation = Animation(pos=(0, 0))
        animation += Animation(pos=(0, height - 100))
        animation += Animation(pos=(width - 100, height - 100))
        animation += Animation(pos=(width - 100, 0))
        animation += Animation(pos=(0, height - 100))
        animation += Animation(pos=(width - 100, height - 100))
        animation += Animation(pos=(width - 100, 0))


        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)

    def build(self):
        # the root is created in pictures.kv
        root = self.root

        def delete_camera():
            root.remove_widget(self.my_camera)

        def build_camera():
            picture_text = Label(text="[color=343d46]Look at the camera[/color]",markup = True,  font_size='80sp', size_hint=(1, 1.8))
            root.add_widget(picture_text)

            def start_button(self):
                loading_pic = Picture(source='Assets/loading.gif', pos=(self.parent.width /2 - self.width /2, 400))
                start.disabled = True;
                moveBlock()

                @mainthread
                def create_loading_gif():
                    root.add_widget(loading_pic)
                                                  
                @mainthread
                def delete_loading_gif():
                    root.remove_widget(loading_pic)

                def create_dataset():

                    path3 = r'selected'
                    for file in os.listdir('selected'):
                        if file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.png'):
                            os.remove(path3+ "/" + file)

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
                    #for filename in glob(join(dirname(__file__), 'OwnDataset', '*')):
                    #for file in os.listdir('OwnDataset'):
                    while(True):
                        ret, img = cam.read()
                        #ret, img = file, True


                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
						#Variable: parameters of detectMultiScale, gray is the image, scaleFactor and minNeighbors
                        faces = detector.detectMultiScale(gray, 1.05, 12)
                        
                        for (x,y,w,h) in faces:
                            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                            #incrementing sample number 
                            sampleNum=sampleNum+1
                            #Variable: fotoSource contains the directory the taken photos will be written to
                            #saving the captured face in the dataset folder
                            fotoSource = "dataSet/User."+Id +'.'+ str(sampleNum) 
                            cv2.imwrite(fotoSource + ".jpg", gray[y:y+h,x:x+w])

                            #create mirror image
                            dsFoto = cv2.imread(fotoSource + ".jpg")
                            vertical_img = dsFoto.copy()
                            vertical_img = cv2.flip(dsFoto, 1)
                            cv2.imwrite(fotoSource + "mirror" + ".jpg", vertical_img)
                            print("mirror created");

                            #create rotated image
                            dsFoto = cv2.imread(fotoSource + ".jpg")
                            rotated = dsFoto.copy()
                            (h, w) = rotated.shape[:2]
                            center = (w/2, h/2)

                            M = cv2.getRotationMatrix2D(center, 5, 1.0)
                            rotated_img = cv2.warpAffine(rotated, M,(w, h))
                            cv2.imwrite(fotoSource + "Rrotated" + ".jpg", rotated_img)
                            print("rotation created");
                            M = cv2.getRotationMatrix2D(center, 355, 1.0)
                            rotated_img = cv2.warpAffine(rotated, M,(w, h))
                            cv2.imwrite(fotoSource + "Lrotated" + ".jpg", rotated_img)
                            print("rotation2 created");
                            


                        #cv2.imshow('Face',img)
                        #wait for 100 miliseconds
                            
                        if cv2.waitKey(1000) & 0xFF == ord('q'):
                           
                            break
                        # break if the sample number is morethan ...
                        elif sampleNum >=13:
                            
                            break
                    delete_camera()
                    root.remove_widget(animation_button)
                    create_loading_gif()
                    root.remove_widget(picture_text)
                    trainner.train()
                    print("TRAINED 1")
                    KivyCamera.CancelUpdate(self)
                    ImageList = detector_img.recog(False)
                    print("DETECTED CLASS")
                    DataRecreation.Recreate(self, ImageList)
                    print("DATA FROM RESULTS")
                    trainner.train()
                    print("TRAINED 2")
                    detector_img.recog(True)
                    print("DETECT NEW CLASS")

                    root.remove_widget(start)
                    delete_loading_gif()
                    build_picturescreen()
                t = threading.Thread(target=create_dataset)
                t.start()
            cap = cv2.VideoCapture(0)
            self.capture = cap
            self.my_camera = KivyCamera(capture=self.capture, fps=60)

            def build_button(self):
                # create a button, and  attach animate() method as a on_press handler
                width = GetSystemMetrics(0)
                height = GetSystemMetrics(1)
                button = Button(size_hint=(None, None),
                                background_normal='',
                                size=(100, 100),
                                pos=((width / 2) - 50, (height / 2) - 50),
                                on_press=self.animate)
                self.animate(button)
                return button

            animation_button = build_button(self)
            def moveBlock():
                root.add_widget(animation_button)


            start = Button(text="Scan your face", size=(3,3), font_size='30sp', size_hint=(0.15,0.1),pos_hint={'center_x': 0.5, 'center_y': 0.1} )
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
            picture_text = Label(text="[color=343d46]Pictures[/color]", markup = True,  font_size='80sp', size_hint=(0.23, 1.8))
            root.add_widget(picture_text)
            buy_button = Button(text='[color=c0c5ce]Buy[/color]', font_size='50sp', markup = True, pos_hint={'x': 0.82, 'y': 0.05}, size_hint=(0.15,0.1))
            root.add_widget(buy_button)
            exit_button = Button(text='[color=c0c5ce]Exit[/color]',markup = True, font_size='50sp', pos_hint={'x': 0.03, 'y': 0.05}, size_hint=(0.15,0.1))
            exit_button.bind(on_press=exit_session)
            root.add_widget(exit_button)

            #Variable: size is the size of the box where all the pictures will be added to
            layout = ScrollView(size_hint=(None, None), size=(930, 630), pos_hint={'center_x': 0.5, 'center_y': .525}, do_scroll_x=False)
            #Variable: cols is the amount of pictures on each row, changing this may require changes in the picture.kv
            box = GridLayout(cols=3, size_hint_y=None)
            box.bind(minimum_height=box.setter("height"))
            layout.add_widget(box)
            root.add_widget(layout)

            # get any files into images directory
            curdir = dirname(__file__)
            counter = 100
            counter2 = 100

			#Variable: the second parameter of join is the directory om the matched images
            for filename in glob(join(curdir, 'img_results', '*')):

                try:
                    # load the image
                    picture = Picture(source=filename, rotation=randint(0, 0), pos=(counter2,counter))
                    counter = counter + 150
                    if counter > 700:
                        counter = 100
                        counter2 = counter2 + 150

                    #picture.on_touch_down(self.root)
                    # add to the main field

                    box.add_widget(picture)
                 
                except FileNotFoundError as e:
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

    def CancelUpdate(self):
        global updates
        updates.cancel()
    
    def update(self, dt):
		#Variable: these CascadeClassifier method show the rectangles on the camera
        face_cascade = cv2.CascadeClassifier('hc/haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('hc/haarcascade_eye_tree_eyeglasses.xml')
        ret, frame = self.capture.read()
        
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
		#Variable: parameters of detectMultiScale, gray is the image, scaleFactor and minNeighbors
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
