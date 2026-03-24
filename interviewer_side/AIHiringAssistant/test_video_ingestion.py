
import cv2
import os
import sys
import numpy as np

# Add the project root to sys.path to import core modules
sys.path.append(os.getcwd())

from core.camera_manager import CameraManager



def log_to_file(msg):
    with open("debug_log.txt", "a") as f:
        f.write(msg + "\n")

def create_dummy_video(filename):
    log_to_file(f"DEBUG: Starting create_dummy_video for {filename}")
    # Create a dummy video file
    height, width = 480, 640
    # Try MJPG which is usually available
    fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
    # Use .avi for MJPG
    filename = filename.replace('.mp4', '.avi')
    log_to_file(f"DEBUG: Creating VideoWriter object for {filename}")
    video = cv2.VideoWriter(filename, fourcc, 10, (width, height))

    if not video.isOpened():
        log_to_file("DEBUG: VideoWriter failed to open!")
        return None

    log_to_file("DEBUG: Writing frames...")
    for i in range(20):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        # Draw a moving circle
        cv2.circle(frame, (30 + i*10, 240), 20, (0, 255, 0), -1)
        video.write(frame)

    log_to_file("DEBUG: Releasing video...")
    video.release()
    log_to_file(f"Created dummy video at {filename}")
    return filename

def test_camera_manager():
    # Clear log file
    with open("debug_log.txt", "w") as f:
        f.write("Starting test...\n")

    # 1. Create a dummy video in user_data
    user_data_dir = os.path.join(os.getcwd(), "user_data")
    os.makedirs(user_data_dir, exist_ok=True)
    video_path = os.path.join(user_data_dir, "test_video.mp4")
    
    # Generate dummy video
    log_to_file("DEBUG: Calling create_dummy_video...")
    actual_path = create_dummy_video(video_path)
    
    if not actual_path:
        log_to_file("Failed to create video.")
        return

    # 2. Initialize CameraManager with the file path
    log_to_file(f"Initializing CameraManager with video file: {actual_path}...")
    try:
        cam = CameraManager(actual_path)
    except Exception as e:
        log_to_file(f"Error initializing CameraManager: {e}")
        return

    # 3. Read frames
    frame_count = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            break
        frame_count += 1
    
    log_to_file(f"Read {frame_count} frames from video.")
    
    if frame_count > 0:
        log_to_file("PASS: CameraManager successfully read from video file.")
    else:
        log_to_file("FAIL: CameraManager failed to read from video file.")

    cam.release()

if __name__ == "__main__":
    test_camera_manager()
