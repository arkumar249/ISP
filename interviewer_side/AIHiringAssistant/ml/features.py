# features.py
# --------------------------------
# Converts a session thermal CSV (wide format) into a fixed-length
# time-aware feature vector using stimulus blocks.
# --------------------------------

import pandas as pd
import numpy as np
from datetime import datetime

# Stimulus blocks within ONE loop (seconds)
STIMULUS_BLOCKS = [
    ("baseline", 0.0, 3.0),
    ("structure", 4.0, 5.0),
    ("velocity", 6.0, 8.0),
    ("fire", 9.0, 11.0),
    ("abstract", 12.0, 24.0),
    ("shock", 25.0, 31.0),
]

LOOP_DURATION = 31.0  # seconds

def extract_features(session_csv_path):
    """
    Input:
        CSV path with columns:
            timestamp (ISO format)
            nose_tip_mean, nose_tip_std, etc.
            
    Output:
        X: 1D numpy array
        feature_names
    """
    try:
        df = pd.read_csv(session_csv_path)
    except Exception as e:
        print(f"Error reading CSV {session_csv_path}: {e}")
        return np.array([]), []

    if df.empty:
        return np.array([]), []

    # Parse timestamp to relative seconds
    try:
        # Try ISO format first
        df['dt'] = pd.to_datetime(df['timestamp'])
    except:
        # Fallback if timestamp is already seconds (compatibility)
        df['dt'] = pd.to_numeric(df['timestamp'], errors='coerce')
        
    if pd.api.types.is_datetime64_any_dtype(df['dt']):
        start_time = df['dt'].iloc[0]
        df['elapsed'] = (df['dt'] - start_time).dt.total_seconds()
    else:
        # Assume it's already relative seconds or just use index as proxy if bad
        df['elapsed'] = df['dt']

    features = []
    feature_names = []

    # Map of logical ROI name to CSV columns
    # Note: ThermalProcessor outputs: {region}_mean, {region}_std
    rois = ["nose_tip", "left_eye", "right_eye", "forehead"]

    # Determine how many loops exist
    max_time = df['elapsed'].max()
    if pd.isna(max_time): max_time = 0
    num_loops = int(max_time // LOOP_DURATION) + 1

    for loop_idx in range(num_loops):
        loop_start = loop_idx * LOOP_DURATION
        
        for block_name, t_start, t_end in STIMULUS_BLOCKS:
            abs_start = loop_start + t_start
            abs_end = loop_start + t_end

            # Filter rows for this block
            block_df = df[
                (df["elapsed"] >= abs_start) &
                (df["elapsed"] <= abs_end)
            ]

            for roi in rois:
                mean_col = f"{roi}_mean"
                std_col = f"{roi}_std"

                if mean_col in df.columns and std_col in df.columns:
                    if block_df.empty:
                        mean_val = 0.0
                        std_val = 0.0
                    else:
                        mean_val = block_df[mean_col].mean()
                        std_val = block_df[std_col].mean()
                else:
                    # Column missing
                    mean_val = 0.0
                    std_val = 0.0

                features.extend([mean_val, std_val])
                feature_names.extend([
                    f"loop{loop_idx+1}_{block_name}_{roi}_mean",
                    f"loop{loop_idx+1}_{block_name}_{roi}_std"
                ])

    X = np.array(features, dtype=float)
    
    # Handle NaNs if any (e.g. empty blocks)
    X = np.nan_to_num(X)
    
    return X, feature_names

# Sanity test
if __name__ == "__main__":
    import os
    # Check for a sample in data/output_logs
    log_dir = "../../data/output_logs"
    if os.path.exists(log_dir):
        files = [f for f in os.listdir(log_dir) if f.endswith(".csv")]
        if files:
            path = os.path.join(log_dir, files[-1])
            print(f"Testing with {path}")
            X, names = extract_features(path)
            print("Feature vector length:", len(X))
            print("First 10 features:", dict(zip(names[:10], X[:10])))
        else:
            print("No CSV files found in logs.")
    else:
        print("Log directory not found.")