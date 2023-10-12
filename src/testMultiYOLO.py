import cv2

def display_rtmp_streams(rtmp_urls):
    # 创建多个cv2.VideoCapture对象，每个对象对应一个RTMP流
    video_captures = [cv2.VideoCapture(url) for url in rtmp_urls]

    while True:
        for idx, cap in enumerate(video_captures):
            ret, frame = cap.read()  # 从当前流中捕获帧
            if not ret:
                print(f"Failed to grab frame from stream {idx}")
                continue

            window_name = f"Stream {idx}"
            cv2.imshow(window_name, frame)  # 显示帧

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # 释放所有VideoCapture对象并关闭所有窗口
    for cap in video_captures:
        cap.release()
    cv2.destroyAllWindows()

# 你的RTMP流列表
rtsp_urls = [
    "rtsp://admin:ydzm1984@192.168.1.64:554/h264/ch1/main/av_stream",
    "pcdc.mp4",
    "pcdc.mp4",
]

display_rtmp_streams(rtsp_urls)
