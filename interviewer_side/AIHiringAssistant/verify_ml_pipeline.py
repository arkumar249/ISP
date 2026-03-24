import numpy as np
import os
import sys

print("Starting verification pipeline (CONSOLE)...")

# Ensure ml_stage is in path
sys.path.append(os.path.join(os.getcwd()))

try:
    print("Importing modules...")
    from ml_stage.model import train_model
    from ml_stage.predict import predict_personality
    from ml_stage.features import extract_features
    print("Modules imported.")

    def verify_pipeline():
        print("Creating dummy training data...")
        log_dir = "../../data/output_logs"
        # Since we are running from root, adjust path
        if os.path.basename(os.getcwd()) == "AIHiringAssistant":
             log_dir = "data/output_logs"
        
        print(f"Looking for logs in: {log_dir}")
        if not os.path.exists(log_dir):
            print("Log dir not found")
            return

        files = [f for f in os.listdir(log_dir) if f.endswith(".csv")]
        if not files:
            print("No logs found")
            return
            
        sample_log = os.path.join(log_dir, files[0])
        print(f"Using sample log: {sample_log}")
        
        X_sample, _ = extract_features(sample_log)
        
        if X_sample.size == 0:
            print("Feature extraction returned empty. Cannot determine input size.")
            return

        n_features = X_sample.shape[0]
        print(f"Feature size: {n_features}")
        
        # Create dummy data
        X_train = np.random.rand(10, n_features)
        Y_train = np.random.rand(10, 5) # 5 OCEAN scores
        
        print("Training dummy model...")
        model_out = "ml_stage/ocean_mlp_model.pkl"
        train_model(X_train, Y_train, model_path=model_out)
        
        print(f"Model trained at {model_out}")
        
        print("Testing prediction...")
        result = predict_personality(sample_log, model_path=model_out)
        print(f"Prediction result: {result}")
        
        if result:
            print("VERIFICATION SUCCESSFUL")
        else:
            print("VERIFICATION FAILED")

    verify_pipeline()

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
