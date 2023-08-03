from kivy.app import App
from kivy.uix.camera import Camera

class MyApp(App):
    def build(self):
        return Camera(play=True)

MyApp().run()
