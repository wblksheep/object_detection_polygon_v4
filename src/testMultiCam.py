import multiprocessing as mp
import time

import cv2


def image_put(q, ip, channel=1):
    cap = cv2.VideoCapture(f"{ip}")
    if cap.isOpened():
        print('HIKVISION')
    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)


def image_get(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        cv2.imshow(window_name, frame)
        cv2.waitKey(1)

def run_single_camera():
    mp.set_start_method(method='spawn')
    queue = mp.Queue(maxsize=2)
    ip1 = "rtmp://122.224.127.166:30002/live/openUrl/DwtDKyQ"
    ip2 = ip1
    processes = [mp.Process(target=image_put, args=(queue, ip1)),
                 mp.Process(target=image_get, args=(queue, ip2))]
    [process.start() for process in processes]
    [process.join() for process in processes]

def run_multi_camera():
    mp.set_start_method(method='spawn')
    camera_ip_l = [
        "rtmp://122.224.127.166:30002/live/openUrl/odIa6NW",
        "rtmp://122.224.127.166:30002/live/openUrl/odIa6NW"
    ]
    queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]
    processes = []
    for queue, camera_ip in zip(queues, camera_ip_l):
        processes.append(mp.Process(target=image_put, args=(queue, camera_ip)))
        processes.append(mp.Process(target=image_get, args=(queue, camera_ip)))
    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()

if __name__ == '__main__':
    run_multi_camera()
    pass
