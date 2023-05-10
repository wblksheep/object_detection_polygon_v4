import cv2
import os
import tempfile

def capture_image():
    # Open the default camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        raise ValueError("Could not open the camera. Please check if the camera is connected properly.")

    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Release the camera
    cap.release()

    # Check if the frame was captured successfully
    if not ret:
        raise ValueError("Could not capture the frame. Please check if the camera is working properly.")

    # Save the captured frame to a temporary file
    _, temp_file_path = tempfile.mkstemp(prefix='captured_image_', suffix='.jpg')
    cv2.imwrite(temp_file_path, frame)

    return temp_file_path
