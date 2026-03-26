import os
import csv
import numpy as np
import cv2  # You may need to run: pip install opencv-python
from datetime import datetime

def generate_hiring_dataset(video_path, num_sessions=50):
    # --- New Logic: Calculate duration and FPS from video ---
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if fps == 0 or frame_count == 0:
        print("Error: Could not read video properties. Check file integrity.")
        return
        
    duration_sec = frame_count / fps
    total_frames = frame_count
    cap.release()

    print(f"Video detected: {duration_sec:.2f}s at {fps} FPS ({total_frames} total frames)")

    base_dir = "data"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    stimulus_points = ["forehead", "nose_tip", "left_cheek", "right_cheek", "chin"]
    
    print(f"Generating {num_sessions} session folders...")

    for i in range(1, num_sessions + 1):
        session_path = os.path.join(base_dir, f"session_{i}")
        os.makedirs(session_path, exist_ok=True)
        
        # --- 1. Generate physio.csv ---
        csv_file_path = os.path.join(session_path, "physio.csv")
        base_lms = np.random.uniform(100, 500, (68, 2))

        ocean_scores = np.random.rand(5).astype(np.float32)
        O, C, E, A, N = ocean_scores
        
        with open(csv_file_path, 'w', newline='') as f:
            fieldnames = ["frame", "timestamp"]
            for lm_idx in range(68):
                fieldnames.extend([f"lm_{lm_idx}_x", f"lm_{lm_idx}_y"])
            fieldnames.extend(stimulus_points)
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for frame in range(total_frames):
                row = {
                    "frame": frame,
                    "timestamp": datetime.now().isoformat()
                }
                
                jitter = np.random.normal(0, 0.3, (68, 2))
                current_lms = base_lms + jitter
                for idx, (x, y) in enumerate(current_lms):
                    row[f"lm_{idx}_x"] = round(x, 2)
                    row[f"lm_{idx}_y"] = round(y, 2)
                
                row["forehead"] = round(36.5 + 0.5*E + np.random.normal(0, 0.1), 3)
                row["nose_tip"] = round(36.5 + 0.4*N + np.random.normal(0, 0.1), 3)
                row["left_cheek"] = round(36.5 + 0.3*A + np.random.normal(0, 0.1), 3)
                row["right_cheek"] = round(36.5 + 0.3*C + np.random.normal(0, 0.1), 3)
                row["chin"] = round(36.5 + 0.4*O + np.random.normal(0, 0.1), 3)

                writer.writerow(row)

        # --- 2. Generate questionnaire.npy ---
        npy_file_path = os.path.join(session_path, "questionnaire.npy")
        np.save(npy_file_path, ocean_scores)

    print(f"Finished! Created {num_sessions} folders in '{base_dir}/'.")

if __name__ == "__main__":
    # Just put your video file path here
    path_to_video = "interview_video.mp4" 
    generate_hiring_dataset(video_path=path_to_video, num_sessions=5)