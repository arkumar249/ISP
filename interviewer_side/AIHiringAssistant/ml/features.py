import pandas as pd
import numpy as np

def extract_features(csv_path):
    df = pd.read_csv(csv_path)

    features = []
    roi_cols = ["forehead", "nose_tip", "left_cheek", "right_cheek", "chin"]

    for col in roi_cols:
        if col not in df.columns:
            features.extend([np.nan]*3)
            continue

        data = df[col].dropna()

        if len(data) == 0:
            features.extend([np.nan]*3)
        else:
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