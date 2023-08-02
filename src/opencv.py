import random
import numpy as np
import cv2
import torch
from yolov5.models.experimental import attempt_load
# from yolov5.utils.general import non_max_suppression
from yolov5.utils.general import non_max_suppression, check_img_size, scale_boxes
from yolov5.utils.augmentations import letterbox


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]  # random color
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))  # coordinates
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

# Load the YOLOv5 model
model = attempt_load('src/models/yolov5s.pt')  # adjust to your model path
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device).eval()

# Start the webcam
cap = cv2.VideoCapture(0)  # if you have multiple webcams, you may need to adjust the number

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the image
    im = np.stack([letterbox(x, 640, stride=32, auto=True)[0] for x in frame])  # resize
    im = im[..., ::-1].transpose((0, 3, 1, 2))  # BGR to RGB, BHWC to BCHW
    im = np.ascontiguousarray(im)  # contiguous
    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = im
    img = torch.from_numpy(im).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 图像归一化
    img_tensor = torch.from_numpy(img).float().to(device)
    img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0)  # BGR to RGB, to 3x416x416
    img_tensor /= 255.0  # 0 - 255 to 0.0 - 1.0

    # Do the inference
    pred = model(img_tensor, augment=False)[0]
    pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=None)

    # Draw the results on the original image
    for i, det in enumerate(pred):
        if len(det):
            # Rescale boxes from img_size to original size
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img.shape).round()

            # Print results to screen
            for *xyxy, conf, cls in reversed(det):
                label = '%s %.2f' % (model.names[int(cls)], conf)
                plot_one_box(xyxy, img, label=label, color='red')

    # Display the image
    cv2.imshow('YOLOv5 Webcam', img)
    if cv2.waitKey(1) == ord('q'):  # press q to quit
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
