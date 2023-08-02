import numpy as np
import cv2
from scipy import interpolate
import matplotlib.pyplot as plt


class PolygonObserver:
    def update(self, points):
        pass


class PolygonSubject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer: PolygonObserver):
        self.observers.append(observer)

    def notify_observers(self, polygon):
        for observer in self.observers:
            observer.update_polygon(polygon)


class Polygon(PolygonSubject):
    def __init__(self, canvas, points=None, img_shape=(1080, 1920)):
        super().__init__()
        self.canvas = canvas
        self.points = points if points else []
        self.curves = []
        self.img_shape = img_shape
        self.mask = np.zeros(img_shape, dtype=np.uint8)
        self.homography_matrix = np.zeros((3, 3), dtype=np.uint8)
        self.control_points = []

        # for x, y in self.points:
        #     point = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='white', outline='black')
        #     self.control_points.append(point)

        self.dragging_point = None
        self.update_polygon()
    def clear_control_point(self):
        self.control_points = []
    def clear_point(self):
        self.points = []
    def control_points_is_empty(self):
        return not self.control_points

    def add_control_point(self, point):
        self.control_points.append(point)

    def add_point(self, point):
        self.points.append(point)

    def generate_mask(self):
        self.mask = np.zeros(self.img_shape, dtype=np.uint8)
        pts = np.array(self.points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.fillPoly(self.mask, [pts], 255)

    def is_point_inside(self, point):
        return self.mask[point[1], point[0]] == 255

    def to_list(self):
        return self.points

    def update_polygon(self):
        self.notify_observers(self)

    def find_dragging_point(self, event_x, event_y):
        for i, point in enumerate(self.control_points):
            x1, y1, x2, y2 = self.canvas.coords(point)
            if x1 <= event_x <= x2 and y1 <= event_y <= y2:
                return i
        return None

    def generate_homography_matrix(self):
        quad_vertices = np.array(self.points, dtype=np.float32)
        rect_width, rect_height = 300, 200
        rect_vertices = np.array([[0, 0], [rect_width, 0], [rect_width, rect_height], [0, rect_height]],
                                 dtype=np.float32)
        self.homography_matrix, _ = cv2.findHomography(quad_vertices, rect_vertices)

    def update_control_point(self, index, x, y):
        self.canvas.coords(self.control_points[index], x - 5, y - 5, x + 5, y + 5)
        self.points[index] = (x, y)
        self.generate_mask()
        self.generate_homography_matrix()
        # # 使用matplotlib将NumPy数组显示为灰度图像
        # plt.imshow(self.mask, cmap='gray')
        # # 保存图像
        # plt.savefig('image_from_numpy_array.png', bbox_inches='tight', pad_inches=0)
        self.update_polygon()

    def clear_dragging_point(self):
        self.dragging_point = None
