import json
import cv2
import numpy as np
from matplotlib import pyplot as plt

with open("polygon.json", "r") as f:
    polygon = json.load(f)
print(polygon)
my_mat = np.load("display1_homography_matrix.npy")
my_mask = np.load("display1_mask.npy")
point = np.array(polygon['display1']['polygon'])
origin = polygon['display1']['origin']
point = np.array(point, dtype=np.int32)
point[:, 0] = point[:, 0] - origin[0]
point[:, 1] = point[:, 1] - origin[1]
while True:
    # 生成一个随机点的坐标
    random_x = np.random.randint(640)
    random_y = np.random.randint(480)
    if my_mask[random_y, random_x] == 255:
        point = np.vstack((point, np.array((random_x, random_y))))
        print(point)
        # 将点转换为齐次坐标
        points_homogeneous = np.column_stack((point, np.ones(point.shape[0])))

        # 应用单应性矩阵
        transformed_points_homogeneous = np.dot(my_mat, points_homogeneous.T).T
        transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
        transformed_points = transformed_points.astype(np.int32)

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
        # 创建一个200*300的空白图像
        screen = np.zeros((200, 300, 3), dtype="uint8")
        # 定义点的大小
        radius = 5
        # 显示图像
        for points in transformed_points:
            cv2.circle(screen, (points[0], 200 - points[1]), radius, (0, 255, 0), -1)

        cv2.imshow('Image with Point', screen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
