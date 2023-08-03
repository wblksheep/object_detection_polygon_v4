import cv2
from ultralytics import YOLO
import os

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# Load the YOLOv8 model
model = YOLO('models/yolov8s.pt')

# Open the video file
# video_path = 0
video_path = "rtmp://rtmp01open.ys7.com:1935/v3/openlive/K03667893_1_1?expire=1722081714&id=606939758247530496&t=53c53c7f999bf9f19183ec9c9dd1fa8d76d6891d7a35fd4ccb8fdf9b2c220067&ev=100"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
