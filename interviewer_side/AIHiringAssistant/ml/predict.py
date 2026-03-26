import joblib
import numpy as np
from features import extract_features

def predict(csv_path):
    model, y_mean, y_std = joblib.load("model.pkl")

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

    traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

    print("\n🔮 Predicted Personality Scores:")
    for t, v in zip(traits, pred):
        print(f"{t}: {v:.3f}")

    return pred