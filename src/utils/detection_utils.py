import cv2
import torch
from pathlib import Path
from .camera_utils import capture_image
from src.detection.yolo_v5 import YOLOv5

# 初始化目标检测模型
model_path = Path("models/yolov5s.pt")
yolo_model = YOLOv5(model_path)

def detect_objects(image_path):
    # 加载图像
    image = cv2.imread(image_path)

    # 执行目标检测
    results = yolo_model.detect(image)

    # 返回检测结果
    return results.xyxy[0].tolist()

def is_point_inside_polygon(point, polygon):
    return cv2.pointPolygonTest(polygon, tuple(point), False) >= 0

def filter_objects_inside_polygon(detection_results, polygon):
    objects_inside_polygon = []

    for detection in detection_results:
        x1, y1, x2, y2, conf, cls = detection
        center = [(x1 + x2) / 2, (y1 + y2) / 2]

        if is_point_inside_polygon(center, polygon):
            objects_inside_polygon.append(detection)

    return objects_inside_polygon
