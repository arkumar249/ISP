from build_dataset import build_dataset
from sklearn.model_selection import KFold
from model import train_model
import numpy as np

def cross_validate(data_dir="data", k=5):
    X, Y = build_dataset(data_dir)

    kf = KFold(n_splits=k, shuffle=True, random_state=42)

    scores = []

    for fold, (train_idx, val_idx) in enumerate(kf.split(X)):
        print(f"\n--- Fold {fold+1} ---")

        X_train, X_val = X[train_idx], X[val_idx]
        Y_train, Y_val = Y[train_idx], Y[val_idx]

        model = train_model(X_train, Y_train)

        # normalize val targets using train stats
        y_mean = Y_train.mean(axis=0)
        y_std = Y_train.std(axis=0) + 1e-8
        Y_val_norm = (Y_val - y_mean) / y_std

        score = model.score(X_val, Y_val_norm)
        print(f"Fold score: {score:.4f}")
        scores.append(score)

    print("\n=== Final CV Results ===")
    print(f"Mean score: {np.mean(scores):.4f}")
    print(f"Std dev: {np.std(scores):.4f}")

if __name__ == "__main__":
    cross_validate()