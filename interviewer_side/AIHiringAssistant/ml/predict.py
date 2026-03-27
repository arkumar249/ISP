import os
import joblib
import numpy as np
from ml.features import extract_features

def predict(csv_path):
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model, y_mean, y_std = joblib.load(model_path)

    X = extract_features(csv_path)

    if X.size == 0:
        print("❌ ERROR: No features extracted. Check your CSV.")
        return None

    X = X.reshape(1, -1)

    # Handle NaNs
    if np.isnan(X).any():
        col_means = np.nanmean(X, axis=0)
        inds = np.where(np.isnan(X))
        X[inds] = np.take(col_means, inds[1])

    # Predict (normalized)
    pred_norm = model.predict(X)[0]

    # Convert back to original scale
    pred = pred_norm * y_std + y_mean

    # Scale predictions into 1-5 range:
    # 1) Normalize to 0-1 using the training target range
    pred_min = pred.min()
    pred_max = pred.max()
    if pred_max - pred_min > 0:
        pred_01 = (pred - pred_min) / (pred_max - pred_min)
    else:
        pred_01 = np.full_like(pred, 0.5)
    # 2) Map to 1-5
    pred = 1.0 + pred_01 * 4.0

    traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

    print("\n🔮 Predicted Personality Scores:")
    for t, v in zip(traits, pred):
        print(f"{t}: {v:.3f}")

    return pred