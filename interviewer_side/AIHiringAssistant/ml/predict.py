# predict.py
# --------------------------------
# Predict OCEAN scores for a new session
# --------------------------------

import os
import joblib
import numpy as np
try:
    from ml_stage.features import extract_features
except ImportError:
    # Direct execution fallback
    from features import extract_features

# Default paths relative to this script
MODEL_PATH = "ocean_mlp_model.pkl"

def predict_personality(session_csv_path, model_path=None):
    """
    Predicts OCEAN scores for a given session CSV.
    
    Args:
        session_csv_path (str): Path to the session CSV file.
        model_path (str, optional): Path to the trained model file. Defaults to 'ocean_mlp_model.pkl'.
        
    Returns:
        dict: A dictionary containing OCEAN scores, or None if prediction fails.
    """
    if model_path is None:
        # Determine absolute path to model relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, MODEL_PATH)

    if not os.path.exists(model_path):
        print(f"Model file not found at: {model_path}")
        return None

    if not os.path.exists(session_csv_path):
        print(f"Session CSV not found at: {session_csv_path}")
        return None

    try:
        model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    try:
        # Extract features (adjust based on your feature extraction logic)
        X, feature_names = extract_features(session_csv_path)
        
        if X.size == 0:
            print("Feature extraction failed or returned empty vector.")
            return None

        # Reshape for single sample prediction
        X = X.reshape(1, -1)

        # Predict
        prediction = model.predict(X)[0]

        ocean = {
            "Openness": round(float(prediction[0]), 2),
            "Conscientiousness": round(float(prediction[1]), 2),
            "Extraversion": round(float(prediction[2]), 2),
            "Agreeableness": round(float(prediction[3]), 2),
            "Neuroticism": round(float(prediction[4]), 2)
        }
        
        return ocean

    except Exception as e:
        print(f"Prediction error: {e}")
        return None


if __name__ == "__main__":
    # Test with the latest logs if available
    base_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base_dir, "../../data/output_logs")
    
    latest_csv = None
    if os.path.exists(log_dir):
        files = [f for f in os.listdir(log_dir) if f.endswith(".csv") and f.startswith("session_")]
        if files:
            files.sort(reverse=True)
            latest_csv = os.path.join(log_dir, files[0])
            
    if latest_csv:
        print(f"Testing prediction on latest log: {latest_csv}")
        result = predict_personality(latest_csv)
        if result:
            print("\nPredicted Personality Profile:")
            print("-" * 30)
            for k, v in result.items():
                print(f"{k.ljust(20)}: {v}")
            print("-" * 30)
    else:
        print("No CSV files found to test prediction.")