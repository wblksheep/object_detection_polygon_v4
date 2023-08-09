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
img_path = "jr.jpeg"
img = cv2.imread(img_path)

# Loop through the video frames
while True:
    # Run YOLOv8 inference on the frame
    results = model(img)
    my_results = MyResults(results[0])

    # Visualize the results on the frame
    annotated_frame = my_results.plot()
    pred_boxes = my_results.results.boxes
    names = my_results.results.names
    radius = 5
    for d in reversed(pred_boxes):
        # print(d.boxes)
        x1, y1, x2, y2 = d.boxes.data[0][:4]
        x, y = int((x1 + x2) / 2), int((y1 + y2) / 2)
        c, conf, id = int(d.cls), float(d.conf), None if d.id is None else int(d.id.item())
        name = ('' if id is None else f'id:{id} ') + names[c]
        label = (f'{name} {conf:.2f}' if conf else name)
        cv2.circle(img, (x, y), radius, (0, 255, 0), -1)

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)
    cv2.imshow("YOLOv8 reference", img)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cv2.destroyAllWindows()
