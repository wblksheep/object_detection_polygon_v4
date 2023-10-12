import cv2
import threading
from ultralytics import YOLO
import multiprocessing


class VideoCapture:
    def __init__(self, src):
        self.src = src
        self.is_capturing = multiprocessing.Value('b', False)
        self.frame_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()

    def start(self):
        self.is_capturing.value = True
        multiprocessing.Process(target=self._capture_loop).start()
        multiprocessing.Process(target=self._yolo_loop).start()

    def _capture_loop(self):
        cap = cv2.VideoCapture(self.src)  # Create VideoCapture object here
        while self.is_capturing.value:
            ret, frame = cap.read()
            if ret:
                self.frame_queue.put(frame)
        cap.release()  # Release the VideoCapture object here

    def _yolo_loop(self):
        model = YOLO('yolov8s.pt')
        while self.is_capturing.value:
            frame = self.frame_queue.get()
            results = model(frame)
            annotated_frame = results[0].plot()
            self.result_queue.put(annotated_frame)

    def get_frame(self):
        if not self.result_queue.empty():
            return self.result_queue.get()
        else:
            return None

    def stop(self):
        self.is_capturing.value = False
        self.cap.release()


def main():
    # IP地址列表
    ip_cameras = ["rtsp://admin:sysren12345@192.168.10.234:554/h264/ch1/main/av_stream",
                  "rtsp://admin:sysren12345@192.168.10.232:554/h264/ch1/main/av_stream",
                  "rtsp://admin:systen12345@192.168.10.231:554/h264/ch1/main/av_stream"]

    # 为每个IP摄像头创建一个VideoCapture实例
    cameras = [VideoCapture(ip) for ip in ip_cameras]

    for camera in cameras:
        camera.start()

    while True:
        # 获取帧，例如：
        frame1 = cameras[0].get_frame()
        frame2 = cameras[1].get_frame()
        frame3 = cameras[2].get_frame()
        if frame1 is not None and frame2 is not None and frame3 is not None:
            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference1", frame1)
            cv2.imshow("YOLOv8 Inference2", frame2)
            cv2.imshow("YOLOv8 Inference3", frame3)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # 帧为空，可以选择跳过或者采取其他措施
            pass


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
