import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ultralytics import YOLO
import os


os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# Load the YOLOv8 model
class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.model = YOLO('models/yolov8s.pt')
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Run YOLOv8 inference on the frame
            results = self.model(frame)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            # OpenCV图像通常使用BGR颜色模式，但Kivy使用RGB模式，因此需要颜色转换
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            buf1 = cv2.flip(annotated_frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(annotated_frame.shape[1], annotated_frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            # 更新纹理
            self.texture = image_texture

class CamApp(App):
    def build(self):
        capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100')
        return KivyCamera(capture=capture, fps=30)

if __name__ == '__main__':
    CamApp().run()
