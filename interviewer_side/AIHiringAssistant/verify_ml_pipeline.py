import os
import joblib

def verify():
    # Attempt to load model and print its path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "ml", "model.pkl")
    print(f"Model path: {model_path}")
    if os.path.exists(model_path):
        print("Model file exists!")
        try:
            model = joblib.load(model_path)
            print("Successfully loaded model!")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("Model file does NOT exist at this path!")
        
    # Attempt to use the UI components headless (if possible) or just test imported predict
    from ml.predict import predict
    
    # Check if we have any test CSVs
    csv_logs = os.path.join(base_dir, "data", "output_logs")
    if os.path.exists(csv_logs):
        csv_files = [f for f in os.listdir(csv_logs) if f.endswith('.csv')]
        if csv_files:
            test_csv = os.path.join(csv_logs, csv_files[-1])
            print(f"\nTesting predict() with: {test_csv}")
            try:
                result = predict(test_csv)
                print(f"Prediction result: {result}")
            except Exception as e:
                print(f"Prediction failed: {e}")
        else:
            print("No CSV files found for testing.")

if __name__ == "__main__":
    verify()
