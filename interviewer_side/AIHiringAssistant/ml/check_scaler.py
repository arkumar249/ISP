import joblib
import numpy as np

model, y_mean, y_std = joblib.load("model.pkl")

scaler = model.named_steps["scaler"]
with open("scaler.txt", "w", encoding="utf-8") as f:
    f.write(f"Scaler Mean: {np.round(scaler.mean_, 3)}\n")
    f.write(f"Scaler Scale (Std): {np.round(scaler.scale_, 3)}\n")
