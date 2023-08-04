import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import OptionProperty, NumericProperty, ListProperty, \
    BooleanProperty
from kivy.lang import Builder
from ultralytics import YOLO
# import os
#
#
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
#加载YOLOv8模型

Builder.load_string('''
<KivyCamera>:
    canvas:
        Color:
            rgba: 0, 1, 0, root.alpha_controlline
        Line:
            points: self.points
            close: self.close

''')
class KivyCamera(Image):
    d = 10
    points = ListProperty([[300, 300], [600, 300], [600, 500], [300, 500]])
    linewidth = NumericProperty(5.0)
    alpha_controlline = NumericProperty(1.0)
    close = BooleanProperty(True)
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.model = YOLO('models/yolov8s.pt')
        self._current_point = None
        # Clock.schedule_interval(self.update, 1.0 / fps)

    def on_touch_down(self, touch):
        if super(KivyCamera, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            for i in range(len(self.points)):
                p = self.points[i]
                if (abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
                        abs(touch.pos[1] - self.pos[1] - p[1]) < self.d):
                    self._current_point = i + 1
                    return True
            return super(KivyCamera, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if super(KivyCamera, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            c = self._current_point
            if c:
                # self.points[c - 1][0] = touch.pos[0] - self.pos[0]
                # self.points[c - 1][1] = touch.pos[1] - self.pos[1]
                self.points[c - 1] = touch.pos
                return True
            return super(KivyCamera, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if super(KivyCamera, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            if self._current_point:
                self._current_point = None
                return True
            return super(KivyCamera, self).on_touch_up(touch)
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
        # capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100')
        capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1721444018&id=604265066984841216&t=66f51dfbc5ed29dafa60634ee6083a59271bd4b7f185bcdb0df9676e424cba63&ev=100')
        return KivyCamera(capture=capture, fps=30)

if __name__ == '__main__':
    CamApp().run()
