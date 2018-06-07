import kivy
kivy.require('1.0.7')

from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from win32api import GetSystemMetrics
from kivy.core.window import Window

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
    
class TestApp(App):

    def animate(self, instance):

        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos=(0, 0))
        animation += Animation(pos=(0, height-100))
        animation += Animation(pos=(width-100, height-100))
        animation += Animation(pos=(width-100, 0))
        animation += Animation(pos=((width / 2) - 50, (height / 2) - 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)

    def build(self):
        # create a button, and  attach animate() method as a on_press handler
        button = Button(size_hint=(None, None),
                        background_normal='',
                        size=(100,100),
                        pos=((width / 2) - 50, (height / 2) - 50),
                        on_press=self.animate)
        
        return button


if __name__ == '__main__':
    Window.size = (1920, 1080)
    Window.fullscreen = "auto"
    TestApp().run()

