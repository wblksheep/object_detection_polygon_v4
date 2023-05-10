import numpy as np
from scipy.optimize import linear_sum_assignment
from collections import deque


class ObjectTracker:
    def __init__(self, max_age=30, min_hits=3, iou_threshold=0.3):
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold
        self.track_id = 0
        self.tracks = []

    def _iou(self, box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2
        xi1, yi1, xi2, yi2 = max(x1, x2), max(y1, y2), min(x1 + w1, x2 + w2), min(y1 + h1, y2 + h2)
        intersection_area = max(xi2 - xi1, 0) * max(yi2 - yi1, 0)
        box1_area, box2_area = w1 * h1, w2 * h2
        union_area = box1_area + box2_area - intersection_area
        return intersection_area / union_area

    def _associate_detections_to_trackers(self, detections):
        iou_matrix = np.zeros((len(detections), len(self.tracks)), dtype=np.float32)

        for d, det in enumerate(detections):
            for t, trk in enumerate(self.tracks):
                iou_matrix[d, t] = self._iou(det, trk['bbox'])

        matched_indices = linear_sum_assignment(-iou_matrix)
        matched_indices = np.asarray(matched_indices)
        matched_indices = np.transpose(matched_indices)

        return matched_indices, iou_matrix

    def update(self, detections):
        matched_indices, iou_matrix = self._associate_detections_to_trackers(detections)

        for trk in self.tracks:
            trk['age'] += 1

        for d, trk_idx in matched_indices:
            if iou_matrix[d, trk_idx] < self.iou_threshold:
                continue

            self.tracks[trk_idx]['bbox'] = detections[d]
            self.tracks[trk_idx]['age'] = 0
            self.tracks[trk_idx]['hits'] += 1

        # Remove old tracks
        self.tracks = [trk for trk in self.tracks if trk['age'] <= self.max_age]

        # Add new detections as new tracks
        for det in detections:
            if all(iou_matrix[d, :] < self.iou_threshold for d, _ in enumerate(det)):
                new_track = {'bbox': det, 'age': 0, 'hits': 1, 'id': self.track_id}
                self.track_id += 1
                self.tracks.append(new_track)

        # Filter out tracks with not enough hits
        self.tracks = [trk for trk in self.tracks if trk['hits'] >= self.min_hits]

        return [trk['bbox'] for trk in self.tracks]
