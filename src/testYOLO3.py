import cv2
import numpy as np
# Open the video file
img_path = "kun.jpeg"
img = cv2.imread(img_path)

img2 = np.ones(img.shape, np.uint8) * 255

img2[]