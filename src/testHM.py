import cv2
import numpy as np
import matplotlib.pyplot as plt

# # 定义单应性矩阵
# homography_matrix = np.array([[1.4, 0.2, 30],
#                               [0.1, 1.3, 20],
#                               [0, 0, 1]])
homography_matrix = np.load("homography_matrix.npy")
# 定义一组点
points = np.float32([[300, 300], [450, 150], [660, 300], [450, 450]])

# 将点转换为齐次坐标
points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))

# 应用单应性矩阵
transformed_points_homogeneous = np.dot(homography_matrix, points_homogeneous.T).T
transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]

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
