from scipy.interpolate import interp1d
from scipy import interpolate
import numpy as np

class BSpline:
    def __init__(self, points):
        self.points = points
        self.update_curve()
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update_curve(self)

    def get_curve_points(self):
        return self.curve_points

    def update_curve(self):
        x = [p[0] for p in self.points]
        y = [p[1] for p in self.points]

        # 计算B样条曲线上的点
        tck = interpolate.splrep(x, y, k=3)
        x_bspline = np.linspace(x[0], x[-1], 1000)
        y_bspline = interpolate.splev(x_bspline, tck)

        # 用计算得到的点绘制曲线
        interp_func = interp1d(x_bspline, y_bspline)
        points = [(x_bspline[i], interp_func(x_bspline[i])) for i in range(len(x_bspline))]
        self.curve_points = points
