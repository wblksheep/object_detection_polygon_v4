import cv2
import numpy as np

# 读取图片
image_path = 'kun.jpeg'
image = cv2.imread(image_path)

# 获取图片的高度和宽度
height, width = image.shape[:2]

# 生成一个随机点的坐标
random_x = np.random.randint(width)
random_y = np.random.randint(height)

# 在图像上绘制这个随机点
cv2.circle(image, (random_x, random_y), radius=5, color=(0, 255, 0), thickness=-1)

# 在图像上添加坐标文本
coordinate_text = f"({random_x}, {random_y})"
cv2.putText(image, coordinate_text, (random_x + 10, random_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# 绘制一条从坐标原点到随机点的线
cv2.line(image, (0, 0), (random_x, random_y), color=(255, 0, 0), thickness=2)

# 显示图像
cv2.imshow('Random Point and Line', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
