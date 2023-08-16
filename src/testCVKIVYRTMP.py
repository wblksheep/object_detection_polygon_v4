import json

import cv2
import requests
from kivy.app import App
from kivy.graphics import Line, Color
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ultralytics import YOLO


from src.myresults import MyResults
# import os
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
#加载YOLOv8模型
class KivyCamera(Image):
    url = 'http://zns.china-yd.com:20001/monitor/getHKMonitorUrl'
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'sessionId=d185b9ec-6a65-4651-af5a-43428e8f37f2',
        'Accept': 'application/json',
    }
    data = {
        "brokerId": 2,
        "cameraIndexCode": "",
        "protocol": "rtmp",
        "streamType": 0,
        "transmode": 1
    }
    def __init__(self, index="0", fps=30.0, name='firstWindow', **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.data["cameraIndexCode"] = index
        self.rtmp = self.getRTMP()
        self.capture = None
        self.model = YOLO('models/yolov8s-seg.pt')
        self.name = name
        self.bind(norm_image_size=self.update_line, pos=self.update_line, size=self.update_line)
        with self.canvas.after:  # ensure the line is drawn above the image
            Color(1, 0, 0, 1)  # set color to red
            self.line = Line(width=2)
        self.retries = 0 # 初始化重连尝试次数
        self.max_retries = 3 # 设置最大重连尝试次数
        # Clock.schedule_interval(self.update, 1.0 / fps)
    def getRTMP(self):
        response = requests.post(self.url, json=self.data, headers=self.headers)
        res = json.loads(response.text)
        res = json.loads(res['data'])
        return res["url"]
    def update_line(self, instance, value):
        # compute the position and size of the image within the widget
        image_x = self.x + (instance.width - self.norm_image_size[0]) / 2
        image_y = self.y + (instance.height - self.norm_image_size[1]) / 2
        self.line.rectangle = (image_x, image_y, *self.norm_image_size)
        print(f'image_x:{image_x}, image_y:{image_y}, norm_image_size:{self.norm_image_size}, instance.pos:{instance.pos}, instance.size:{instance.size}')
        return image_x, image_y, self.norm_image_size

    def updateRTMP(self):
        self.capture = cv2.VideoCapture(self.rtmp)
        # 连续读取多个帧以清空缓冲区
        for _ in range(350):  # 你可以根据需求调整循环次数
            ret, frame = self.capture.read()
    def update(self, dt, polygon, rect_width=300, rect_height=200):
        ret, frame = self.capture.read()
        if not ret:
            print("连接中断，重新连接...")
            self.capture.release()
            self.retries += 1  # 增加尝试计数器
            # if self.retries > self.max_retries:
            #     print("超过最大尝试次数，停止重连。")
            #     self.retries = 0  # 重置重连尝试计数，以便下一次可能的重连
            #     self.updateRTMP()
            #     return None, True  # 退出函数，不再尝试
            self.capture = cv2.VideoCapture(self.rtmp)
            return None, False
        else:
            # Run YOLOv8 inference on the frame
            results = self.model(frame)

            # # Visualize the results on the frame
            # annotated_frame = results[0].plot()
            my_results = MyResults(results[0], self.name)
            # Visualize the results on the frame
            annotated_frame, ret_points = my_results.plot(masks=False, rect_width=rect_width, rect_height=rect_height, image_shape=polygon[f"{self.name}"]['image_shape'], origin=polygon[f"{self.name}"]['origin'])
            # OpenCV图像通常使用BGR颜色模式，但Kivy使用RGB模式，因此需要颜色转换
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            buf1 = cv2.flip(annotated_frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(annotated_frame.shape[1], annotated_frame.shape[0]), colorfmt='rgb')
            image_texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            # 更新纹理
            self.texture = image_texture
            return ret_points, False

class CamApp(App):
    def build(self):
        capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100')
        # capture = cv2.VideoCapture('rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1721444018&id=604265066984841216&t=66f51dfbc5ed29dafa60634ee6083a59271bd4b7f185bcdb0df9676e424cba63&ev=100')
        # capture = cv2.VideoCapture(0)
        return KivyCamera(capture=capture, fps=30)

if __name__ == '__main__':
    CamApp().run()
