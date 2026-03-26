import os
import csv
import numpy as np
from datetime import datetime

def generate_hiring_dataset(num_sessions=50, duration_sec=61, fps=30):
    total_frames = duration_sec * fps
    base_dir = "data"
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    print(f"Generating {num_sessions} session folders...")

    for i in range(1, num_sessions + 1):
        session_path = os.path.join(base_dir, f"session_{i}")
        os.makedirs(session_path, exist_ok=True)
        
        csv_file_path = os.path.join(session_path, "physio.csv")

        # Generate personality
        ocean_scores = np.random.rand(5).astype(np.float32)
        O, C, E, A, N = ocean_scores

        base_lms = np.random.uniform(100, 500, (68, 2))

        with open(csv_file_path, 'w', newline='') as f:
            fieldnames = ["frame", "timestamp"]

            # landmarks
            for lm_idx in range(68):
                fieldnames.extend([f"lm_{lm_idx}_x", f"lm_{lm_idx}_y"])

            # 🔥 EXACT MATCH TO YOUR REAL FORMAT
            fieldnames.extend([
                "nose_tip_mean", "nose_tip_std",
                "left_eye_mean", "left_eye_std",
                "right_eye_mean", "right_eye_std",
                "forehead_mean", "forehead_std"
            ])

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # session-level base temp
            base_temp = 36.3 + np.random.normal(0, 0.2)

            for frame in range(total_frames):
                row = {
                    "frame": frame,
                    "timestamp": datetime.now().isoformat()
                }

                # landmarks
                jitter = np.random.normal(0, 0.3, (68, 2))
                current_lms = base_lms + jitter
                for idx, (x, y) in enumerate(current_lms):
                    row[f"lm_{idx}_x"] = round(x, 2)
                    row[f"lm_{idx}_y"] = round(y, 2)

                # 🔥 personality-driven mean values
                row["forehead_mean"] = base_temp + 0.5 * E + np.random.normal(0, 0.07)
                row["nose_tip_mean"] = base_temp + 0.4 * N + np.random.normal(0, 0.07)
                row["left_eye_mean"] = base_temp + 0.3 * A + np.random.normal(0, 0.07)
                row["right_eye_mean"] = base_temp + 0.3 * C + np.random.normal(0, 0.07)

                # 🔥 std values (small variation, also slightly personality influenced)
                row["forehead_std"] = abs(np.random.normal(0.1 + 0.05*E, 0.02))
                row["nose_tip_std"] = abs(np.random.normal(0.1 + 0.05*N, 0.02))
                row["left_eye_std"] = abs(np.random.normal(0.1 + 0.05*A, 0.02))
                row["right_eye_std"] = abs(np.random.normal(0.1 + 0.05*C, 0.02))

                writer.writerow(row)

        # save questionnaire
        np.save(os.path.join(session_path, "questionnaire.npy"), ocean_scores)

    print(f"Finished! Created {num_sessions} sessions in '{base_dir}/'.")


if __name__ == "__main__":
    generate_hiring_dataset()