import cv2
import numpy as np

# 读取图像
img_path = "kun.jpeg"
image = cv2.imread(img_path)

if image is None:
    print("Image not loaded")
else:
    print("Image loaded successfully")
# image = cv2.imread("kun.jpeg")
# 定义单应性矩阵
H = np.array([[1.4, 0.2, -100],
              [0.1, 1.5, -50],
              [0.001, 0, 1]])

# 定义参考点（例如图像的四个角）
pts = np.array([[0, 0],
                [image.shape[1]-1, 0],
                [image.shape[1]-1, image.shape[0]-1],
                [0, image.shape[0]-1]], dtype=np.float32)

# 将参考点变换到新坐标
pts_transformed = cv2.perspectiveTransform(pts.reshape(-1, 1, 2), H).astype(np.int32)
pts = pts.astype(np.int32)

# 在原始图像上绘制参考点
for pt in pts:
    cv2.circle(image, tuple(pt), 5, (0, 255, 0), -1)

# 应用单应性变换
warped_image = cv2.warpPerspective(image, H, (image.shape[1], image.shape[0]))

# 在变换后的图像上绘制映射后的点
for pt in pts_transformed:
    cv2.circle(warped_image, tuple(pt[0]), 5, (0, 0, 255), -1)

# 显示原始和变换后的图像
cv2.imshow('Original', image)
cv2.imshow('Warped', warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
