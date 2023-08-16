import json

import cv2
import numpy as np
from matplotlib import pyplot as plt


def generate_mask(points, image_shape=(1440, 2560), origin=(0, 0)):
    mask = np.zeros(image_shape, dtype=np.uint8)
    pts = np.array(points, dtype=np.int32)
    pts[:, 1] = 1440 - pts[:, 1]
    pts[:, 0] = pts[:, 0] - origin[0]
    pts[:, 1] = pts[:, 1] - origin[1]
    pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(mask, [pts], 255)
    return mask
def generate_homography_matrix(points, rect_width, rect_height, origin=(0, 0)):
    pts = np.array(points, dtype=np.int32)
    pts[:, 0] = pts[:, 0] - origin[0]
    pts[:, 1] = pts[:, 1] - origin[1]
    quad_vertices = np.array(pts, dtype=np.float32)
    rect_vertices = np.array([[0, 0], [0, rect_height], [rect_width, rect_height], [rect_width, 0]],
                             dtype=np.float32)
    homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)
    return homography_matrix
# with open("polygon.json", "r") as f:
#     polygon = json.load(f)
# my_mask = np.load("display1_mask.npy")
# my_mat = np.load("display1_homography_matrix.npy")
# points = np.array(polygon['display1']['polygon'])
points = np.array([[544.0, 464.0],[563.0, 983.0],[1070.0, 974.0],[1086.0, 652.0]], dtype=np.float32)
origin = [0, 0]
# my_mat = generate_homography_matrix(points, 300, 200)
p_points = np.array([[56, 0],[56, 1337],[2504, 1377],[2504, 0]], dtype=np.float32)
my_mat = generate_homography_matrix(p_points, 2560, 1440)
print(points)
# 将点转换为齐次坐标
points_homogeneous = np.column_stack((points, np.ones(points.shape[0])))

# 应用单应性矩阵
transformed_points_homogeneous = np.dot(my_mat, points_homogeneous.T).T
transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
transformed_points = transformed_points.astype(np.int32)
my_mask = generate_mask(transformed_points)

# 使用matplotlib将NumPy数组显示为灰度图像
plt.imshow(my_mask, cmap='gray')
# 保存图像
plt.savefig(f'my_mask.png', bbox_inches='tight', pad_inches=0)
my_mat = generate_homography_matrix(transformed_points, 300, 200)
points = transformed_points.astype(np.int32)
points[:, 0] = points[:, 0] - origin[0]
points[:, 1] = points[:, 1] - origin[1]
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
        transformed_points_homogeneous = np.dot(my_mat, points_homogeneous.T).T
        transformed_points = transformed_points_homogeneous[:, :2] / transformed_points_homogeneous[:, 2:]
        transformed_points = transformed_points.astype(np.int32)
# 可视化原始点和变换后的点
plt.figure(figsize=(10, 6))

plt.plot(points[:, 0], points[:, 1], 'bo', label='Original Points')
plt.plot(transformed_points[:, 0], transformed_points[:, 1], 'ro', label='Transformed Points')

# for i in range(points.shape[0]):
#     plt.plot([points[i, 0], transformed_points[i, 0]], [points[i, 1], transformed_points[i, 1]], 'g-')

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

