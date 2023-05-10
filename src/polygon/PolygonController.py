from src.gui.canvas import DetectionCanvas
from src.polygon.polygon import Polygon
class PolygonController:
    def __init__(self, polygon_subject: Polygon, polygon_canvas: DetectionCanvas):
        self.polygon_subject = polygon_subject
        self.polygon_canvas = polygon_canvas

    def on_button_press(self, event_x, event_y):
        dragging_point = self.polygon_subject.find_dragging_point(event_x, event_y)
        if dragging_point is not None:
            self.polygon_subject.dragging_point = dragging_point

    def on_move_press(self, event_x, event_y):
        if self.polygon_subject.dragging_point is not None:
            self.polygon_subject.update_control_point(self.polygon_subject.dragging_point, event_x, event_y)

    def on_button_release(self):
        self.polygon_subject.clear_dragging_point()