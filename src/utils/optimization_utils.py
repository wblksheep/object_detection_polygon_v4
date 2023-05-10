import cv2
import numpy as np

def optimize_polygon_calculation(polygon):
    mask = np.zeros_like(polygon, dtype=np.uint8)
    cv2.fillPoly(mask, [polygon], 255)
    return mask

def select_best_tracking_algorithm(tracking_algorithms, performance_data):
    best_algorithm = None
    best_performance = float('-inf')
    for algorithm in tracking_algorithms:
        accuracy = performance_data[algorithm]["accuracy"]
        speed = performance_data[algorithm]["speed"]
        performance = accuracy * speed
        if performance > best_performance:
            best_performance = performance
            best_algorithm = algorithm
    return best_algorithm


if __name__ == "__main__":
    polygon = np.array([(50, 50), (200, 50), (200, 200), (50, 200)], dtype=np.int32)
    optimized_mask = optimize_polygon_calculation(polygon)
    print(optimized_mask)

    tracking_algorithms = ["SORT", "DeepSORT"]
    performance_data = {
        "SORT": {"accuracy": 0.8, "speed": 1.0},
        "DeepSORT": {"accuracy": 0.9, "speed": 0.8}
    }
    best_algorithm = select_best_tracking_algorithm(tracking_algorithms, performance_data)
    print(best_algorithm)
