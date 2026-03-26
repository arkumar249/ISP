import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import joblib

def train_model(X, Y):
    # Normalize targets (VERY IMPORTANT)
    y_mean = Y.mean(axis=0)
    y_std = Y.std(axis=0) + 1e-8
    Y_norm = (Y - y_mean) / y_std

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(8,),   # small network
            activation="relu",
            solver="adam",

            alpha=0.1,                # strong regularization
            learning_rate_init=0.001,

            max_iter=2000,
            early_stopping=True,
            validation_fraction=0.2,

            n_iter_no_change=40,
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