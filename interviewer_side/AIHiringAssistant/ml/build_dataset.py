# build_dataset.py
# --------------------------------
# Builds training dataset (X_train, Y_train)
# from session CSVs (in data/output_logs) and questionnaire outputs
# --------------------------------

import os
import numpy as np
try:
    from ml_stage.features import extract_features
except ImportError:
    # Direct execution fallback
    from features import extract_features


# -------- CONFIGURATION --------
# Adjusted path to point to output_logs relative to this script
SESSION_DIR = "../../data/output_logs"
QUESTIONNAIRE_DIR = "../../data/questionnaires"

X_OUTPUT_PATH = "X_train.npy"
Y_OUTPUT_PATH = "Y_train.npy"
# --------------------------------


def build_dataset():
    X_list = []
    Y_list = []

    if not os.path.exists(SESSION_DIR):
        print(f"Session directory not found: {SESSION_DIR}")
        return

    session_files = sorted([
        f for f in os.listdir(SESSION_DIR)
        if f.endswith(".csv") and f.startswith("session_")
    ])

    if not session_files:
        raise RuntimeError("No session CSV files found in output_logs.")

    for session_file in session_files:
        # file: session_20260210_141330.csv -> id: session_20260210_141330
        session_id = os.path.splitext(session_file)[0]
        
        session_csv_path = os.path.join(SESSION_DIR, session_file)
        
        # Questionnaire expected: session_20260210_141330.npy
        questionnaire_path = os.path.join(
            QUESTIONNAIRE_DIR,
            f"{session_id}.npy"
        )

        if not os.path.exists(questionnaire_path):
            print(f"[SKIP] No questionnaire for {session_id} (Expected at: {questionnaire_path})")
            continue

        # -------- Extract X --------
        print(f"Processing {session_id}...")
        X, feature_names = extract_features(session_csv_path)

        if X.size == 0:
            print(f"[SKIP] Failed to extract features for {session_id}")
            continue

        # -------- Load Y --------
        try:
            Y = np.load(questionnaire_path)
        except Exception as e:
            print(f"[SKIP] Error loading Y for {session_id}: {e}")
            continue

        if Y.shape != (5,):
            print(f"[SKIP] Invalid questionnaire shape for {session_id}: {Y.shape}")
            continue

        X_list.append(X)
        Y_list.append(Y)

        print(f"[OK] Added session {session_id}")

    if not X_list:
        print("No valid paired sessions found (CSV + Questionnaire). Cannot build dataset.")
        return

    X_train = np.vstack(X_list)
    Y_train = np.vstack(Y_list)

    np.save(X_OUTPUT_PATH, X_train)
    np.save(Y_OUTPUT_PATH, Y_train)

    print("\nDataset built successfully")
    print("X_train shape:", X_train.shape)
    print("Y_train shape:", Y_train.shape)
    print("Saved to:")
    print(" ", os.path.abspath(X_OUTPUT_PATH))
    print(" ", os.path.abspath(Y_OUTPUT_PATH))


# -------- Run manually --------
if __name__ == "__main__":
    build_dataset()