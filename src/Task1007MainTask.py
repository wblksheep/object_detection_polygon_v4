import asyncio
import json
import threading
import websockets
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
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
        Button:
            size_hint: None, None
            size: 100, 44
            text:'Screen3'
            on_release: root.change_screen3(self)
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
            id:animatebutton
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

    def change_screen3(self, button):
        self.manager.current = 'display3'


class DisplayScreen(Screen):
    d = 100  # 拖动区域的能力大小
    capture = ObjectProperty(None)
    fps = NumericProperty(30.0)
    points = ListProperty([[56, 0], [56, 1377], [2504, 1377], [2504, 0]])
    linewidth = NumericProperty(3)
    _current_point = None

    def __init__(self, rtsp=0, uri=8760, **kwargs):
        super(DisplayScreen, self).__init__(**kwargs)
        self.reconnect = False
        self.ret_points = None
        self.camera = KivyCamera(rtsp=rtsp, fps=30.0, name=self.name)
        self.ids.boxlayout.add_widget(self.camera)
        self._update_points_animation_ev = None
        p = []
        for point in self.points:
            p.append(list(point))
        with open("polygon.json", "r") as f:
            content = f.read().strip()
            if not content:
                print('File is empty')
                self.polygon = {}
            else:
                self.polygon = json.loads(content)
                if f'{self.name}' in self.polygon:
                    self.rect_width = 300 if 'size' not in self.polygon[f'{self.name}'] else \
                    self.polygon[f'{self.name}']['size'][0]
                    self.rect_height = 200 if 'size' not in self.polygon[f'{self.name}'] else \
                    self.polygon[f'{self.name}']['size'][1]
                    for i in range(4):
                        self.points[i] = self.polygon[f'{self.name}']['polygon'][i]
        self.bind(size=self.update_line)
        self.websocket_thread = threading.Thread(target=self.start_sending_data, args=(uri,))
        self.websocket_thread.start()

    async def send_data_to_uri(self, uri):
        # 循环发送数据
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    if self.ret_points is not None:
                        bias = self.polygon[f'{self.name}']['bias']
                        self.ret_points[:, 0] = self.ret_points[:, 0] + bias[0]
                        self.ret_points[:, 1] = self.ret_points[:, 1] + bias[1]
                        points = self.ret_points.tolist()
                    else:
                        points = [[]]
                    data_to_send = json.dumps({f'{self.name}': points}) if points else ""
                    await websocket.send(data_to_send)
                    await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                print("Task was cancelled, restarting...")
                continue
            except Exception as e:
                print(f"Error occurred: {e}")
                continue

    def start_sending_data(self, uri="ws://47.98.235.96:20030/webserver/python/1"):
        # 创建事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # 开始发送数据
        loop.run_until_complete(self.send_data_to_uri(uri))

    def update_line(self, instance, value):
        image_x, image_y, image_size = self.camera.update_line(instance, value)

    def change_screen(self, button):
        self.manager.current = 'control'

    def save_polygon(self, button):
        p = []
        for point in self.points:
            p.append(list(point))
        if f'{self.name}' in self.polygon:
            self.polygon[f'{self.name}']['polygon'] = p
            self.rect_width = int(self.ids.rect_width.text) if self.ids.rect_width.text else \
            self.polygon[f'{self.name}']['size'][0] if 'size' in self.polygon[f'{self.name}'] else 300
            self.rect_height = int(self.ids.rect_height.text) if self.ids.rect_height.text else \
            self.polygon[f'{self.name}']['size'][1] if 'size' in self.polygon[f'{self.name}'] else 200
            self.polygon[f'{self.name}']['size'] = [self.rect_width, self.rect_height]
        else:
            self.polygon[f'{self.name}'] = {'polygon': p, 'image_shape': [1440, 2560], 'origin': [0, 0], 'bias': [0, 0],
                                            'size': [300, 200]}
        with open("polygon.json", "w+") as f:
            json.dump(self.polygon, f, indent=4)
        self.rect_width = self.polygon[f'{self.name}']['size'][0]
        self.rect_height = self.polygon[f'{self.name}']['size'][1]
        image_shape = self.polygon[f'{self.name}']['image_shape']
        points = np.array(self.polygon[f'{self.name}']['polygon'])
        p_points = np.array([[56, 0], [56, 1377], [2504, 1377], [2504, 0]], dtype=np.float32)
        first_mat = self.generate_homography_matrix(p_points, 2560, 1440)
        # 将点转换为齐次坐标
        points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))
        # 应用单应性矩阵
        transformed_points_homogeneous = np.dot(first_mat, points_homogeneous.T).T
        transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
        transformed_points = transformed_points.astype(np.int32)
        my_mask = self.generate_mask(transformed_points)
        second_mat = self.generate_homography_matrix(transformed_points, self.rect_width, self.rect_height)
        np.save(f"{self.name}_mask.npy", my_mask)
        np.save(f"{self.name}_first_mat.npy", first_mat)
        np.save(f"{self.name}_second_mat.npy", second_mat)
        # 使用matplotlib将NumPy数组显示为灰度图像
        plt.imshow(my_mask, cmap='gray')
        # 保存图像
        plt.savefig(f'{self.name}_image_from_numpy_array.png', bbox_inches='tight', pad_inches=0)

    def generate_mask(self, points, image_shape=(1440, 2560), origin=(0, 0)):
        mask = np.zeros(image_shape, dtype=np.uint8)
        pts = np.array(points, dtype=np.int32)
        pts[:, 1] = image_shape[0] - 1 - pts[:, 1]
        pts[:, 0] = pts[:, 0] - origin[0]
        pts[:, 1] = pts[:, 1] - origin[1]
        pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
        return mask

    def generate_homography_matrix(self, points, rect_width, rect_height, origin=(0, 0)):
        pts = np.array(points, dtype=np.int32)
        pts[:, 0] = pts[:, 0] - origin[0]
        pts[:, 1] = pts[:, 1] - origin[1]
        quad_vertices = np.array(pts, dtype=np.float32)
        rect_vertices = np.array([[0, 0], [0, rect_height], [rect_width, rect_height], [rect_width, 0]],
                                 dtype=np.float32)
        homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)
        return homography_matrix

    def animate(self, do_animation):
        if do_animation and not self.reconnect:
            self.start_task()
        elif self._update_points_animation_ev is not None or self.reconnect:
            self._update_points_animation_ev.cancel()
            self.ids.animatebutton.state = 'normal'
            self.reconnect = False

    def start_task(self):
        # 在单独的线程中运行长时间任务
        thread = threading.Thread(target=self.background_task)
        thread.start()

    def background_task(self):
        self.camera.updateRTMP()
        self._update_points_animation_ev = Clock.schedule_interval(
            self.update_points_animation, 1.0 / self.fps)

    def update_points_animation(self, dt):
        self.ret_points, self.reconnect = self.camera.update(dt, self.polygon, self.rect_width, self.rect_height)

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
        # 北墙中东向西道路
        sm.add_widget(
            DisplayScreen(name='display1', rtsp="rtsp://admin:sysren12345@192.168.10.234:554/h264/ch1/main/av_stream",
                          uri="ws://47.98.235.96:20030/webserver/python/1"))
        # # 门卫室西向东道路
        # sm.add_widget(
        #     DisplayScreen(name='display2', rtsp="rtsp://admin:sysren12345@192.168.10.34:554/h264/ch1/main/av_stream",
        #                   uri="ws://47.98.235.96:20030/webserver/python/2"))
        # # B楼楼顶广角监控
        # sm.add_widget(
        #     DisplayScreen(name='display3', rtsp="rtsp://admin:sysren12345@192.168.10.232:554/h264/ch1/main/av_stream",
        #                   uri="ws://47.98.235.96:20030/webserver/python/3"))
        return sm


MyApp().run()
