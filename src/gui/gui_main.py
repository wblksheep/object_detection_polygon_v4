import os
import queue
import sys
import numpy as np
from PIL import Image, ImageTk
import json
import cv2
from src.detection.yolo_v5 import YOLOv5
from src.polygon.polygon import Polygon
sys.path.append(os.path.dirname(__file__))
import tkinter as tk
from tkinter import ttk, filedialog, Canvas, NW
from canvas import DetectionCanvas
from src.polygon.PolygonController import PolygonController
import requests


class TargetDetectionGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.yolo = YOLOv5()  #初始化YOLOv5对象
        self.selected_curve = None
        self.create_widgets()
        self.polygon_init = False
        self.polygon_controller = None
        self.capture_image_id = None
        self.data_queue = queue.Queue()


    def create_widgets(self):

        # 创建两个框架
        self.frame1 = tk.Frame(self.master, width=1920, height=1080, background="red")
        # self.frame1 = tk.Frame(self.master, width=5500, height=1600, background="red")
        self.frame2 = tk.Frame(self.master, width=2560, height=200, background="blue")
        self.frame2.grid_propagate(False)
        self.canvas = DetectionCanvas(self.frame1, width=1920, height=1080)
        # self.canvas = DetectionCanvas(self.frame1, width=5120, height=1440)
        self.canvas.place(x=0, y=0)
        self.canvas.bind("<Button-1>", self.click_on_canvas)
        self.canvas.bind("<B1-Motion>", self.on_move_press)  # 绑定鼠标移动事件
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.capture_button = ttk.Button(self.frame2, text="Capture", command=self.toggle_capture)

        self.capture_button.grid(row=0, column=0)
        self.capturing = False
        self.polygon = Polygon(self.canvas)  # 初始化多边形对象
        self.mapped_canvas = Canvas(self.frame2, width=300, height=200)
        self.mapped_canvas.grid(row=0, column=1)
        warped_image = np.zeros((200, 300), dtype=np.uint8)
        warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2RGB)
        warped_image = Image.fromarray(warped_image)
        warped_image = ImageTk.PhotoImage(warped_image)
        self.mapped_canvas.create_image(0, 0, anchor=NW, image=warped_image)
        self.rect_vertices = np.array([[0, 0], [300, 0], [300, 200], [0, 200]],
                                 dtype=np.float32)
        for i in range(4):
            self.mapped_canvas.create_line(self.rect_vertices[i - 1][0], self.rect_vertices[i - 1][1], self.rect_vertices[i][0],
                                      self.rect_vertices[i][1], fill='blue')
        self.mode_combobox = ttk.Combobox(self.frame2, values=["High Performance", "Balanced", "Energy Saving"])
        self.mode_combobox.grid(row=0, column=2)

        self.save_button = ttk.Button(self.frame2, text="Save Results", command=self.save_detection_results)
        self.save_button.grid(row=0, column=3)

        self.load_button = ttk.Button(self.frame2, text="Load Polygon", command=self.load_preset_polygon)
        self.load_button.grid(row=0, column=4)

        self.entry_text = tk.StringVar()  # 创建一个StringVar变量来存储文本框内容
        self.entry = tk.Entry(self.frame2, textvariable=self.entry_text, width=200)  # 创建一个文本框，将StringVar变量绑定到它上面
        self.entry.grid(row=0, column=5)
        # 将两个框架添加到窗口中

        self.frame1.pack(side='top')
        self.frame2.pack(side='bottom')



    def click_on_canvas(self, event):
        if not self.polygon_init:
            point = (event.x, event.y)
            self.polygon.add_point(point)
            point_id = self.canvas.draw_point(point)
            self.polygon.add_control_point(point_id)
            if len(self.polygon.points) == 4:
                self.polygon.register_observer(self.canvas)  #把canvas注册成polygon的observer
                self.polygon_controller = PolygonController(self.polygon,
                                                            self.canvas)
                self.polygon_init = True
                self.polygon_controller.on_button_press(event.x, event.y)
        else:
            self.polygon_controller.on_button_press(event.x, event.y)

    def on_move_press(self, event):
        self.polygon_controller.on_move_press(event.x, event.y)

    def on_button_release(self, event):
        if hasattr(self, 'polygon_controller'):
            self.polygon_controller.on_button_release()

    def toggle_capture(self):
        self.capturing = not self.capturing
        if self.capturing:
            self.capture_button.config(text="Stop")
            self.after(1, self.display_image_on_canvas)
        else:
            self.capture_button.config(text="Capture")

    def display_image_on_canvas(self):

        self.canvas.clear_detections()
        self.mapped_canvas.delete("all")
        for i in range(4):
            self.mapped_canvas.create_line(self.rect_vertices[i - 1][0], self.rect_vertices[i - 1][1], self.rect_vertices[i][0],
                                      self.rect_vertices[i][1], fill='blue')
        if not self.capturing:
            return

        from src.config import load_config
        _, RESOURCES_PATH = load_config()
        # 构建图像文件的绝对路径
        image_path = os.path.join(RESOURCES_PATH, "img.png")
        try:
            sources, im, im0s, frame, stream = next(self.yolo.stream_loader)
        except StopIteration:
            self.yolo.stream_loader.update()
            return


        # 获取canvas的宽度和高度
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 将图像转换为PIL图像
        # pil_image = Image.fromarray(cv2.cvtColor(np.asarray(im0s), cv2.COLOR_BGR2RGB))
        pil_image = Image.fromarray(cv2.cvtColor(np.array(im0s).squeeze(0), cv2.COLOR_BGR2RGB))

        # 缩放图像以适应canvas的大小
        pil_image = pil_image.resize((canvas_width, canvas_height), Image.ANTIALIAS)

        self.canvas_image = ImageTk.PhotoImage(pil_image)
        if self.capture_image_id is None:
            self.capture_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        else:
            self.canvas.itemconfig(self.capture_image_id, image=self.canvas_image)

        self.update_detection_results(frame, im, im0s)
        self.after(1, self.display_image_on_canvas)

    def update_detection_results(self, frame, im, im0s):
        detections = self.yolo.detect(frame, im, im0s)

        frame = cv2.cvtColor(np.array(im0s).squeeze(0), cv2.COLOR_BGR2RGB)
        self.canvas_image = ImageTk.PhotoImage(Image.fromarray(frame))
        self.canvas.itemconfig(self.capture_image_id, image=self.canvas_image)
        for detection in detections:
            self.canvas.draw_detections(detection, self.polygon, self.mapped_canvas, self.data_queue)
        # points = []
        # while not q.empty():
        #     points.append(q.get())
        # json_data = json.dumps({'points': points})
        # response = requests.post('http://localhost:5000/test', json=json_data)
        # print(f'Server response: {response.json()}')
        self.canvas.update_pre_detections()

    def save_detection_results(self):
        # 存储当前的检测结果和多边形参数
        save_path = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")], defaultextension="*.json")
        if save_path:
            results = {
                "detections": self.yolo.detections,
                "polygon": self.polygon.to_list()
            }
            with open(save_path, "w") as f:
                json.dump(results, f)
        pass

    def load_preset_polygon(self):
        # 加载预设置的多边形参数
        load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], defaultextension="*.json")
        if load_path:
            with open(load_path, "r") as f:
                loaded_data = json.load(f)
            self.polygon = Polygon(points=loaded_data["polygon"])
            self.canvas.draw_polygon(self.polygon)
        pass
