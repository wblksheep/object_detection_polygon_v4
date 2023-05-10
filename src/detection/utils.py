import cv2
from .object_tracker import ObjectTracker


def is_point_inside_polygon(point, polygon):
    return cv2.pointPolygonTest(polygon, point, False) >= 0


def apply_tracking_algorithm(detections, tracker=None):
    if tracker is None:
        tracker = ObjectTracker()

    tracked_objects = tracker.update(detections)
    return tracked_objects