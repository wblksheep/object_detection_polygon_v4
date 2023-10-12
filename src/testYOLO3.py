import cv2
from ultralytics import YOLO



# Open the video file
rtsp_url = "rtsp://admin:systen12345@192.168.10.231:554/h264/ch1/main/av_stream"
cap = cv2.VideoCapture(rtsp_url)

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

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
        cv2.imshow("YOLOv8 Inference3", annotated_frame)

        # # Display the annotated frame
        # cv2.imshow("YOLOv8 Inference3", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
