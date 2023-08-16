import json

import cv2
import numpy as np
from matplotlib import pyplot as plt
"""

"""
points = np.array([
            [
                56,
                0
            ],
            [
                56,
                1377
            ],
            [
                2504,
                1377
            ],
            [
                2504,
                0
            ]
        ], dtype=np.float32)
second_mat = np.load("second_mat.npy")
my_mask = np.load("my_mask.npy")
for _ in range(100000):
    random_x = np.random.randint(2560)
    random_y = np.random.randint(1440)

    if my_mask[random_y, random_x] == 255:
        random_y = 1439 - random_y
        points = np.vstack((points, np.array((random_x, random_y))))

        # print(points)
        # 将点转换为齐次坐标
        points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))

        # 应用单应性矩阵
        transformed_points_homogeneous = np.dot(second_mat, points_homogeneous.T).T
        transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
        transformed_points = transformed_points.astype(np.int32)
        # 可视化原始点和变换后的点
        plt.figure(figsize=(10, 6))

        plt.plot(points[:, 0], points[:, 1], 'bo', label='Original Points')
        plt.plot(transformed_points[:, 0], transformed_points[:, 1], 'ro', label='Transformed Points')

        for i in range(points.shape[0]):
            plt.plot([points[i, 0], transformed_points[i, 0]], [points[i, 1], transformed_points[i, 1]], 'g-')

        plt.legend()
        plt.title('Visualization of Points Transformed by Homography Matrix')
        plt.axis('equal')
        plt.show()
        # 创建一个200*300的空白图像
        screen = np.zeros((200, 300, 3), dtype="uint8")
        # 定义点的大小
        radius = 5
        # 显示图像
        for point in transformed_points:
            cv2.circle(screen, (point[0], 200 - point[1]), radius, (0, 255, 0), -1)

        cv2.imshow('Image with Point', screen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



