import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

def train_model(X, Y):
    # Normalize targets (VERY IMPORTANT)
    y_mean = Y.mean(axis=0)
    y_std = Y.std(axis=0) + 1e-8
    Y_norm = (Y - y_mean) / y_std

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_leaf=2,
            random_state=42
        ))
    ])

    model.fit(X, Y_norm)

    # Check training score (on normalized target)
    train_score = model.score(X, Y_norm)
    print(f"Train score: {train_score:.4f}")

    # Save model + normalization info
    joblib.dump((model, y_mean, y_std), "model.pkl")
    print("Model saved as model.pkl")

    return model