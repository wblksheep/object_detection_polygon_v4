# import cv2
# import numpy as np
#
# # 创建一个空白图像
# img = np.zeros((100, 100, 3), dtype=np.uint8)
#
# # 定义要填充的多边形的点
# pts = [np.array([[0, 50], [0, 0], [100, 0], [100, 50]], np.int32),
#        np.array([[50, 50], [60, 60], [50, 60]], np.int32)]
#
# # 将点数组的形状更改为所需的格式
# pts = [pts[0].reshape((-1, 1, 2)), pts[1].reshape((-1, 1, 2))]
#
# # 使用红色填充多边形
# cv2.fillPoly(img, pts, (0, 0, 255))
#
# # 显示图像
# cv2.imshow('Filled Polygons', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
import numpy as np

mask = np.load("mask.npy")
print("hello world")
