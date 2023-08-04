import cv2
from kivy.app import App
from kivy.graphics import Line, Color
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ultralytics import YOLO
import os


os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
#加载YOLOv8模型
class KivyCamera(Image):
    def __init__(self, capture=None, fps=30.0, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.model = YOLO('models/yolov8s.pt')
        self.bind(norm_image_size=self.update_line, pos=self.update_line)
        with self.canvas.after:  # ensure the line is drawn above the image
            Color(1, 0, 0, 1)  # set color to red
            self.line = Line(width=2)
        # Clock.schedule_interval(self.update, 1.0 / fps)
    def update_line(self, instance, value):
        # compute the position and size of the image within the widget
        image_x = self.x + (self.width - self.norm_image_size[0]) / 2
        image_y = self.y + (self.height - self.norm_image_size[1]) / 2
        self.line.rectangle = (image_x, image_y, *self.norm_image_size)

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
        # capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1721444018&id=604265066984841216&t=66f51dfbc5ed29dafa60634ee6083a59271bd4b7f185bcdb0df9676e424cba63&ev=100')
        # capture = cv2.VideoCapture(0)
        return KivyCamera(capture=capture, fps=30)

if __name__ == '__main__':
    CamApp().run()
