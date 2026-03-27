import pandas as pd
import numpy as np

def extract_features(csv_path):
    df = pd.read_csv(csv_path)

    features = []
    # Map the expected 5 regions to the actual thermal generated columns
    roi_cols = ["forehead_mean", "nose_tip_mean", "left_eye_mean", "right_eye_mean", "nose_tip_std"]

    # Check if the CSV uses raw pixel intensities (0-255) instead of Celsius temperatures
    # by evaluating a known temperature column
    is_pixels = False
    if "forehead_mean" in df.columns:
        sample_data = df["forehead_mean"].dropna()
        if len(sample_data) > 0 and sample_data.mean() > 50:
            is_pixels = True

    for col in roi_cols:
        if col not in df.columns:
            features.extend([np.nan]*3)
            continue

        data = df[col].dropna()

        if len(data) == 0:
            features.extend([np.nan]*3)
        else:
            if is_pixels:
                if col.endswith("_std"):
                    data = data * (6.0 / 255.0)
                else:
                    data = 32.0 + (data / 255.0) * 6.0
            # mean + std
            mean_val = data.mean()
            std_val = data.std()

            # diff mean
            if len(data) > 1:
                diff_mean = np.mean(np.diff(data))
            else:
                diff_mean = np.nan

            features.extend([mean_val, std_val, diff_mean])

    return np.array(features, dtype=float)