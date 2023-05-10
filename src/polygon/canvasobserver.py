
class CanvasObserver:
    def __init__(self, canvas, curve):
        self.canvas = canvas
        self.control_points = []
        for x, y in curve.points:
            point = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='white', outline='black')
            self.control_points.append(point)

        curve.register_observer(self)
        self.update_curve(curve)

    def update_curve(self, curve):
        if hasattr(self, 'curve'):
            self.canvas.delete(self.curve)

        coords = [p for point in curve.curve_points for p in point]
        self.curve = self.canvas.create_line(*coords, fill='blue', smooth=True)

        for idx, (x, y) in enumerate(curve.points):
            self.canvas.coords(self.control_points[idx], x-5, y-5, x+5, y+5)