import os
import numpy as np
from features import extract_features

def build_dataset(data_dir):
    X_list, Y_list = [], []

    for folder in os.listdir(data_dir):
        session_path = os.path.join(data_dir, folder)

        if not os.path.isdir(session_path):
            continue

        csv_path = os.path.join(session_path, "physio.csv")
        y_path   = os.path.join(session_path, "questionnaire.npy")

        if not (os.path.exists(csv_path) and os.path.exists(y_path)):
            continue

        X = extract_features(csv_path)
        Y = np.load(y_path)

        if np.any(np.isnan(Y)):
            continue

        X_list.append(X)
        Y_list.append(Y)

    X = np.vstack(X_list)
    Y = np.vstack(Y_list)

    # Handle NaNs properly
    col_means = np.nanmean(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])

    print("Dataset shape:", X.shape, Y.shape)

    return X, Y