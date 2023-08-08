import cv2
import numpy as np

# 创建一个200*300的空白图像
image = np.zeros((200, 300, 3), dtype="uint8")

# 定义点的位置
center_x = 200
center_y = 100

# 定义点的大小
radius = 5

# 在图像上绘制点
cv2.circle(image, (center_x, center_y), radius, (0, 255, 0), -1)

# 显示图像
cv2.imshow('Image with Point', image)
cv2.waitKey(0)
cv2.destroyAllWindows()





