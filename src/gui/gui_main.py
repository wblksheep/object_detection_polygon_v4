import os
import sys

import numpy as np
from PIL import Image, ImageTk
import math
import json
import cv2
import torch
# Import YOLOv5
from src.detection.yolo_v5 import YOLOv5
from src.polygon.polygon import Polygon

sys.path.append(os.path.dirname(__file__))
import tkinter as tk
from tkinter import ttk, filedialog, Canvas, NW
from canvas import DetectionCanvas
from src.polygon.PolygonController import PolygonController


class TargetDetectionGUI(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.yolo = YOLOv5()  # Initialize YOLOv5 object
        self.curve_selected = False  # Add a boolean attribute to represent if a curve is selected
        self.selected_curve = None
        self.create_widgets()
        self.polygon_init = False
        self.polygon_controller = None
        self.capture_image_id = None

    # def create_widgets(self):
    #     self.canvas = DetectionCanvas(self.master, width=800, height=640)
    #     self.canvas.grid(row=0, column=0, rowspan=4)
    #     self.canvas.bind("<Button-1>", self.click_on_canvas)
    #     self.canvas.bind("<B1-Motion>", self.on_move_press)  # Bind mouse move event
    #     self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
    #     self.capture_button = ttk.Button(self.master, text="Capture", command=self.toggle_capture)
    #     self.capture_button.grid(row=0, column=1)
    #     self.capturing = False
    #     self.polygon = Polygon(self.canvas)  # Initialize Polygon object
    #     self.create_sliders()
    #     # Add this piece of code to the create_widgets method in the TargetDetectionGUI class
    #     # mapped_canvas = Canvas(self.master, width=rect_width, height=rect_height)
    #     self.mapped_canvas = Canvas(self.master, width=300, height=200)
    #     self.mapped_canvas.grid(row=0, column=1)
    #     warped_image = np.zeros((200, 300), dtype=np.uint8)
    #     warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2RGB)
    #     warped_image = Image.fromarray(warped_image)
    #     warped_image = ImageTk.PhotoImage(warped_image)
    #     self.mapped_canvas.create_image(0, 0, anchor=NW, image=warped_image)
    #     self.mode_combobox = ttk.Combobox(self.master, values=["High Performance", "Balanced", "Energy Saving"])
    #     self.mode_combobox.grid(row=2, column=1)
    #
    #     self.save_button = ttk.Button(self.master, text="Save Results", command=self.save_detection_results)
    #     self.save_button.grid(row=3, column=1)
    #
    #     self.load_button = ttk.Button(self.master, text="Load Polygon", command=self.load_preset_polygon)
    #     self.load_button.grid(row=4, column=1)

    # def create_widgets(self):
    #     image = np.zeros((400, 400), dtype=np.uint8)
    #     image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    #     image = Image.fromarray(image)
    #     image = ImageTk.PhotoImage(image)
    #     self.canvas = DetectionCanvas(self.master, width=300, height=300)
    #     self.canvas.grid(row=0, column=0, rowspan=8)
    #     self.canvas.bind("<Button-1>", self.click_on_canvas)
    #     self.canvas.bind("<B1-Motion>", self.on_move_press)  # Bind mouse move event
    #     self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
    #     self.canvas.grid(row=0, column=0)
    #     self.canvas.create_image(0, 0, anchor=NW, image=image)
    #     self.capture_button = ttk.Button(self.master, text="Capture", command=self.toggle_capture)
    #     self.capture_button.grid(row=1, column=1, sticky='w')
    #     self.capturing = False
    #     self.polygon = Polygon(self.canvas)  # Initialize Polygon object
    #     self.create_sliders()
    #     self.mapped_canvas = Canvas(self.master, width=300, height=200)
    #     self.mapped_canvas.grid(row=0, column=1, sticky='w')
    #     # warped_image = cv2.warpPerspective(image, self.polygon.homography_matrix, (300, 200))
    #     warped_image = np.zeros((200, 300), dtype=np.uint8)
    #     warped_image = cv2.cvtColor(warped_image, cv2.COLOR_GRAY2RGB)
    #     warped_image = Image.fromarray(warped_image)
    #     warped_image = ImageTk.PhotoImage(warped_image)
    #     self.mapped_canvas.create_image(0, 0, anchor=NW, image=warped_image)
    #     self.mode_combobox = ttk.Combobox(self.master, values=["High Performance", "Balanced", "Energy Saving"])
    #     self.mode_combobox.grid(row=2, column=1, sticky='w')
    #
    #     self.save_button = ttk.Button(self.master, text="Save Results", command=self.save_detection_results)
    #     self.save_button.grid(row=3, column=1, sticky='w')
    #
    #     self.load_button = ttk.Button(self.master, text="Load Polygon", command=self.load_preset_polygon)
    #     self.load_button.grid(row=4, column=1, sticky='w')

    def create_widgets(self):
        # image = np.zeros((400, 400), dtype=np.uint8)
        # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        # image = Image.fromarray(image)
        # image = ImageTk.PhotoImage(image)
        self.canvas = DetectionCanvas(self.master, width=1500, height=600)  # Changed from self.master to self
        self.canvas.grid(row=0, column=0, rowspan=8)
        self.canvas.bind("<Button-1>", self.click_on_canvas)
        self.canvas.bind("<B1-Motion>", self.on_move_press)  # Bind mouse move event
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.grid(row=0, column=0)
        # self.canvas.create_image(0, 0, anchor=NW, image=image)
        self.capture_button = ttk.Button(self, text="Capture", command=self.toggle_capture)  # Changed from self.master to self
        self.capture_button.grid(row=1, column=1, sticky='w')
        self.capturing = False
        self.polygon = Polygon(self.canvas)  # Initialize Polygon object
        self.create_sliders()
        self.mapped_canvas = Canvas(self, width=300, height=200)  # Changed from self.master to self
        self.mapped_canvas.grid(row=0, column=1, sticky='w')
        # warped_image = cv2.warpPerspective(image, self.polygon.homography_matrix, (300, 200))
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
        self.mode_combobox = ttk.Combobox(self, values=["High Performance", "Balanced", "Energy Saving"])  # Changed from self.master to self
        self.mode_combobox.grid(row=2, column=1, sticky='w')

        self.save_button = ttk.Button(self, text="Save Results", command=self.save_detection_results)  # Changed from self.master to self
        self.save_button.grid(row=3, column=1, sticky='w')

        self.load_button = ttk.Button(self, text="Load Polygon", command=self.load_preset_polygon)  # Changed from self.master to self
        self.load_button.grid(row=4, column=1, sticky='w')



    def create_sliders(self):
        self.slider = tk.Scale(self.master, from_=0, to=1, orient=tk.HORIZONTAL, command=self.on_slider_change)
        self.slider.grid(row=1, column=1)

    def on_slider_change(self, value):
        # Update curves based on slider value
        self.polygon.update_curves(float(value))
        self.canvas.update_curves(self.polygon.curves)

    def click_on_canvas(self, event):
        if not self.polygon_init:
            point = (event.x, event.y)
            self.polygon.add_point(point)
            point_id = self.canvas.draw_point(point)
            self.polygon.add_control_point(point_id)
            if len(self.polygon.points) == 4:
                self.polygon.register_observer(self.canvas)  # Register canvas as observer of polygon
                self.polygon_controller = PolygonController(self.polygon,
                                                            self.canvas)  # Initialize PolygonController object                   self.polygon.curves[i])  # Initialize CanvasObserver object
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

    # def display_image_on_canvas(self):
    #
    #     self.canvas.clear_detections()
    #     if not self.capturing:
    #         return
    #
    #     from src.config import load_config
    #     _, RESOURCES_PATH = load_config()
    #     # 构建图像文件的绝对路径
    #     image_path = os.path.join(RESOURCES_PATH, "img.png")
    #     frame = self.yolo.capture_image() if self.yolo.capture_image() is not None else cv2.imread(image_path)
    #     self.canvas_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    #     if self.capture_image_id is None:
    #         self.capture_image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
    #     else:
    #         self.canvas.itemconfig(self.capture_image_id, image=self.canvas_image)
    #
    #     self.update_detection_results(frame, image_path)
    #     self.after(1, self.display_image_on_canvas)
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
        sources, im, im0s, frame, stream = next(self.yolo.stream_loader)

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
            self.canvas.draw_detections(detection, self.polygon, self.mapped_canvas)

        self.canvas.update_pre_detections()
        # self.polygon.update_polygon()

    def save_detection_results(self):
        # Save current detection results and polygon settings
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
        # Load preset polygon settings
        load_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")], defaultextension="*.json")
        if load_path:
            with open(load_path, "r") as f:
                loaded_data = json.load(f)
            self.polygon = Polygon(points=loaded_data["polygon"])
            self.canvas.draw_polygon(self.polygon)
        pass
