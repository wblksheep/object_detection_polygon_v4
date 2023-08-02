import torch
from pathlib import Path
import torchvision.transforms as transforms
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image
import cv2
from yolov5.models.yolo import Model
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
from yolov5.utils.general import non_max_suppression, check_img_size, scale_boxes
from yolov5.utils.dataloaders import LoadImages, LoadStreams
import numpy as np
import os

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'


class YOLOv5:
    def __init__(self, model_path="models/yolov5s.pt"):
        # 设备配置
        self.device = select_device('cuda:0' if torch.cuda.is_available() else 'cpu')
        # self.device = select_device('cpu')
        # 加载模型
        self.model = attempt_load(model_path, device=self.device)
        # # 加载模型
        # self.model = Model(model_path).to(self.device)
        # self.model.load_state_dict(torch.load(model_path, map_location=self.device)['model'])
        # self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s-seg', pretrained=True, path=model_path)
        # Add image transforms
        self.img_transforms = Compose([
            Resize((640, 640)),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        # self.cap = cv2.VideoCapture(0)
        # self.stream_loader = LoadStreams("rtsp://admin:ydzm1984@192.168.1.64:554/Streaming/Channels/1", img_size=640)
        # self.stream_loader = LoadStreams("0", img_size=640)
        # self.stream_loader = LoadStreams("rtmp://122.224.127.166:30002/live/openUrl/l7lh2Ao", img_size=640)
        #ip摄像头位置
        self.stream_loader = LoadStreams("rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1721444018&id=604265066984841216&t=66f51dfbc5ed29dafa60634ee6083a59271bd4b7f185bcdb0df9676e424cba63&ev=100", img_size=640)
        #北墙东向西
        # self.stream_loader = LoadStreams("rtmp://122.224.127.166:30002/live/openUrl/FqK51y8", img_size=640)
        # 先调用 __iter__ 方法来初始化 count 属性
        self.stream_loader.__iter__()

    def capture_image(self):
        return next(self.stream_loader)  # 这行代码会先调用__iter__()，然后再调用__next__()


    def detect_objects(self, img_tensor):
        with torch.no_grad():
            detections = self.model(img_tensor)
        # Apply non-maximum suppression
        nms_results = non_max_suppression(detections, conf_thres=0.25, iou_thres=0.45)
        # Convert the results to a numpy array
        detections_np = [result.cpu().numpy() for result in nms_results]
        return detections_np

    def detect(self, frame, im, im0s, conf_thres=0.25, iou_thres=0.45):
        imgsz = check_img_size(640, s=self.model.stride.max())  # 检查图片大小
        half = self.device.type != 'cpu'  # 半精度只支持GPU

        if half:
            self.model.half()

        # 设置模型为评估模式
        self.model.eval()

        img = torch.from_numpy(im).to(self.device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 图像归一化
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 推理
        with torch.no_grad():
            pred = self.model(img, augment=False)[0]

        # 应用NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres)

        # 处理检测结果
        for i, det in enumerate(pred):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], np.array(im0s).squeeze(0).shape).round()

            # 打印结果
            return det