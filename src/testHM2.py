import cv2
import numpy as np
from matplotlib import pyplot as plt

my_mask = np.load("mask.npy")
my_mat = np.load("homography_matrix.npy")
x, y = 300, 300
if my_mask[y, x] == 255:
    point = np.array([[300, 300], [450, 150], [660, 300], [450, 450], [450, 300], [600, 300], [450, 400]], dtype=np.float32)
    mapped_point = cv2.perspectiveTransform(point[None, :, :], my_mat)
    mapped_x, mapped_y = int(mapped_point[0, 0, 0]), int(mapped_point[0, 0, 1])
    # 将点转换为齐次坐标
    points_homogeneous = np.column_stack((point, np.ones(point.shape[0])))

    # 应用单应性矩阵
    transformed_points_homogeneous = np.dot(my_mat, points_homogeneous.T).T
    transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
    # 可视化原始点和变换后的点
    plt.figure(figsize=(10, 6))

    plt.plot(point[:, 0], point[:, 1], 'bo', label='Original Points')
    plt.plot(transformed_points[:, 0], transformed_points[:, 1], 'ro', label='Transformed Points')

    for i in range(point.shape[0]):
        plt.plot([point[i, 0], transformed_points[i, 0]], [point[i, 1], transformed_points[i, 1]], 'g-')

    plt.legend()
    plt.title('Visualization of Points Transformed by Homography Matrix')
    plt.axis('equal')
    plt.show()