import json

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.clock import Clock
import cv2
import numpy as np
from matplotlib import pyplot as plt

from src.testCVKIVYRTMP import KivyCamera

Builder.load_string('''
<ControlScreen>:
    GridLayout:
        cols: 2
        size_hint: 1, None
        height: 44 * 5
        
        Button:
            size_hint: None, None
            size: 100, 44
            text:'Screen1'
            on_release: root.change_screen1(self)
        Button:
            size_hint: None, None
            size: 100, 44
            text:'Screen2'
            on_release: root.change_screen2(self)
        # ToggleButton:
        #     size_hint: None, None
        #     size: 100, 44
        #     text: 'Animate'
        #     on_state: root.animate(self.state == 'down')
            
<DisplayScreen>:
    BoxLayout:
        id:boxlayout
        canvas.after:
            Color:
                rgba: 0, 1, 0, 1  # Green
            Line:
                points: root.points
                width: root.linewidth
                close: True

        
    GridLayout:
        cols: 2
        size_hint: 1, None
        height: 30 * 3
        
        Button:
            text:'Back to Main Screen'
            on_release: root.change_screen(self)
        ToggleButton:
            text: 'Animate'
            on_state: root.animate(self.state == 'down')
        Button:
            text:'Save Polygon'
            on_release: root.save_polygon(self)
        TextInput:
            hint_text: 'Enter the width'
            id:rect_width
        TextInput:
            hint_text: 'Enter the height'
            id:rect_height

''')


class ControlScreen(Screen):
    def __init__(self, **kwargs):
        super(ControlScreen, self).__init__(**kwargs)
        # self.add_widget(Button(text='Go to Display Screen', on_release=self.change_screen))

    def change_screen1(self, button):
        self.manager.current = 'display1'

    def change_screen2(self, button):
        self.manager.current = 'display2'
class DisplayScreen(Screen):
    d = 100  # 拖动区域的能力大小
    capture = ObjectProperty(None)
    fps = NumericProperty(30.0)
    points = ListProperty([[0, 0], [0, 1440], [2560, 1440], [2560, 0]])
    # points = ListProperty([[300, 300], [450, 150], [660, 300], [450, 450]])
    linewidth = NumericProperty(3)
    _current_point = None  # 被拖动的点的下标

    def __init__(self, rtmp=0, **kwargs):
        super(DisplayScreen, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(rtmp)
        # self.capture = cv2.VideoCapture(
        #     'rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100')
        # self.capture = cv2.VideoCapture(
        #     'rtmp://rtmp03open.ys7.com:1935/v3/openlive/724460572_1_1?expire=1722161140&id=607272892865970176&t=a4eb9528c0e1ccea689a4b36ab5b7c30f94516f39670e9f452719e9de8a28103&ev=100')
        self.camera = KivyCamera(capture=self.capture, fps=30.0, name=self.name)
        # self.camera.bind(norm_image_size=self.update_polygon, pos=self.update_polygon)
        self.ids.boxlayout.add_widget(self.camera)
        # self.image = Image(self.camera)
        # self.add_widget(Button(text='Back to Main Screen', on_release=self.change_screen))
        # Clock.schedule_interval(self.update, 1.0 / self.fps)
        self._update_points_animation_ev = None
        self.rect_width = 300
        self.rect_height = 200
        with open("polygon.json", "r") as f:
            content = f.read().strip()
            if not content:
                print('File is empty')
            else:
                polygon = json.loads(content)
                if f'{self.name}' in polygon:
                    for i in range(4):
                        self.points[i] = polygon[f'{self.name}']['polygon'][i]
        self.bind(size=self.update_line)
    def update_line(self, instance, value):
        image_x, image_y, image_size = self.camera.update_line(instance, value)

    # def update_polygon(self, instance, value):
    #     instance.image_x

    # self.bind(size=self.update_layers, pos=self.update_layers)
    # self.labels = []
    # for i in range(len(self.points)):
    #     label = Label(text=str(i), center=self.points[i], color=[1, 0, 0, 1])
    #     self.labels.append(label)
    #     self.add_widget(label)
    # self.camera.bind(texture=self.on_texture)
    # def on_texture(self, instance, value):
    #     self.ids.camera.canvas.ask_update()

    def change_screen(self, button):
        self.manager.current = 'control'

    # def update_layers(self, instance, value):
    #     for point in self.points:
    #
    #     self.bg.pos = instance.pos
    #     self.bg.size = instance.size
    #     self.fg.pos = (self.width / 4, self.height / 4)
    #     self.fg.size = (self.width / 2, self.height / 2)
    def save_polygon(self, button):
        p = []
        for point in self.points:
            p.append(list(point))
        with open("polygon.json", "r") as f:
            content = f.read()
            if not content:
                print('File is empty')
                polygon = {}
            else:
                polygon = json.loads(content)
            polygon[f'{self.name}'] = {'polygon': p}
        with open("polygon.json", "w+") as f:
            json.dump(polygon, f, indent=4)

        self.rect_width = int(self.ids.rect_width.text) if self.ids.rect_width.text else 300
        self.rect_height = int(self.ids.rect_height.text) if self.ids.rect_height.text else 200
        self.generate_homography_matrix(rect_width=self.rect_width, rect_height=self.rect_height)
        self.generate_mask(image_shape=(1440, 2560))
        np.save("mask.npy", self.mask)
        np.save("homography_matrix.npy", self.homography_matrix)
        # 使用matplotlib将NumPy数组显示为灰度图像
        plt.imshow(self.mask, cmap='gray')
        # 保存图像
        plt.savefig('image_from_numpy_array.png', bbox_inches='tight', pad_inches=0)

    def generate_mask(self, image_shape=(1440, 2560)):
        self.mask = np.zeros(image_shape, dtype=np.uint8)
        pts = np.asarray(self.points, dtype=np.int32)
        pts[:, 1] = 1440 - pts[:, 1]
        pts = np.asarray(pts, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(self.mask, [pts], 255)
    def generate_HM_change(self, image_shape=(1440, 2560)):
        quad_vertices = np.array(self.points, dtype=np.float32)
        rect_vertices = np.array([[0, 0], [0, rect_height], [rect_width, rect_height], [rect_width, 0]],
                                 dtype=np.float32)
        self.homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)

    def generate_homography_matrix(self, rect_width, rect_height):

        quad_vertices = np.array(self.points, dtype=np.float32)
        rect_vertices = np.array([[0, 0], [0, rect_height], [rect_width, rect_height], [rect_width, 0]],
                                 dtype=np.float32)
        self.homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)

    def animate(self, do_animation):
        if do_animation:
            self._update_points_animation_ev = Clock.schedule_interval(
                self.update_points_animation, 1.0 / self.fps)
        elif self._update_points_animation_ev is not None:
            self._update_points_animation_ev.cancel()

    def update_points_animation(self, dt):
        self.camera.update(dt, self.rect_width, self.rect_height)

    # def on_enter(self, do_animation):
    #     if do_animation:
    #         self._update_points_animation_ev = Clock.schedule_interval(
    #             self.update_points_animation, 1.0 / self.fps)
    #     elif self._update_points_animation_ev is not None:
    #         self._update_points_animation_ev.cancel()
    #     # self._update_points_animation_ev = Clock.schedule_interval(self.update_points_animation, 1.0 / 30.0)
    #
    # def on_leave(self):
    #     Clock.unschedule(self.event)
    # def update(self, dt):
    #     self.camera.update(dt)
    def on_touch_down(self, touch):
        if super(DisplayScreen, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            for i in range(len(self.points)):
                p = self.points[i]
                if (abs(touch.pos[0] - self.pos[0] - p[0]) < self.d and
                        abs(touch.pos[1] - self.pos[1] - p[1]) < self.d):
                    self._current_point = i + 1
                    return True
            return super(DisplayScreen, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if super(DisplayScreen, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            c = self._current_point
            if c:
                # self.points[c - 1][0] = touch.pos[0] - self.pos[0]
                # self.points[c - 1][1] = touch.pos[1] - self.pos[1]
                self.points[c - 1] = touch.pos
                return True
            return super(DisplayScreen, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if super(DisplayScreen, self).on_touch_down(touch):
            return True
        if self.collide_point(touch.pos[0], touch.pos[1]):
            if self._current_point:
                self.canvas.after
                self._current_point = None
                return True
            return super(DisplayScreen, self).on_touch_up(touch)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ControlScreen(name='control'))
        sm.add_widget(DisplayScreen(name='display1', rtmp=0))
        sm.add_widget(DisplayScreen(name='display2', rtmp='rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100'))
        return sm


MyApp().run()
