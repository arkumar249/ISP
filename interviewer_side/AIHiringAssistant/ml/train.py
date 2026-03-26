from build_dataset import build_dataset
from model import train_model
from sklearn.model_selection import train_test_split
import numpy as np

def main():
    data_dir = "data"

    print("Building dataset...")
    X, Y = build_dataset(data_dir)

    # Split dataset
    X_train, X_val, Y_train, Y_val = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    print("Training model...")
    model = train_model(X_train, Y_train)

    # Normalize validation targets using TRAIN stats
    y_mean = Y_train.mean(axis=0)
    y_std = Y_train.std(axis=0) + 1e-8
    Y_val_norm = (Y_val - y_mean) / y_std

    # Validation score
    val_score = model.score(X_val, Y_val_norm)
    print(f"Validation score: {val_score:.4f}")

if __name__ == "__main__":
    main()