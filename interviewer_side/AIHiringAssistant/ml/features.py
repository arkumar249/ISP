import pandas as pd
import numpy as np

def extract_features(csv_path):
    df = pd.read_csv(csv_path)

    roi_cols = ["nose_tip", "left_eye", "right_eye", "forehead"]
    features = []

    for roi in roi_cols:
        mean_col = f"{roi}_mean"
        std_col = f"{roi}_std"

        if mean_col in df.columns:
            data = df[mean_col].dropna()
            features.append(data.mean())
            features.append(data.std())
        else:
            features.extend([np.nan, np.nan])

        if std_col in df.columns:
            data = df[std_col].dropna()
            features.append(data.mean())
        else:
            features.append(np.nan)

    return np.array(features, dtype=float)