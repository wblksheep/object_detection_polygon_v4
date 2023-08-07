import cv2
from ultralytics import YOLO
from ultralytics.engine.results import Results
from pathlib import Path
from src.myresults import MyResults

# import os
#
# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'

# Load the YOLOv8 model
model = YOLO('models/yolov8s-seg.pt')

# Open the video file
img_path = "kun.jpeg"
img = cv2.imread(img_path)

# Loop through the video frames
while True:
    # Run YOLOv8 inference on the frame
    results = model(img)
    my_results = MyResults(results[0])

    # Visualize the results on the frame
    annotated_frame = my_results.plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)
    p = Path('kun2.jpeg')
    if not p.exists():
        cv2.imwrite("kun2.jpeg", annotated_frame)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
