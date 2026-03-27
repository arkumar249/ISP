"""
bootstrap_train.py
------------------
Three-step pipeline:
  STEP 1 - Generate bootstrapped data from 6 real sessions and save to disk
  STEP 2 - Load saved data and train MLP model  -> model.pkl
  STEP 3 - Evaluate accuracy and print full report

Usage (from /ml directory):
    python bootstrap_train.py
"""

import os
import sys
import numpy as np
import joblib
import openpyxl
import warnings
warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from features import extract_features
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, r2_score

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
DATA_SESSION_DIR  = os.path.join(SCRIPT_DIR, "data", "session")
SCORE_FILE        = os.path.join(SCRIPT_DIR, "data", "score", "score.xlsx")
BOOTSTRAP_DIR     = os.path.join(SCRIPT_DIR, "data", "bootstrapped")
X_AUG_PATH        = os.path.join(BOOTSTRAP_DIR, "X_augmented.npy")
Y_AUG_PATH        = os.path.join(BOOTSTRAP_DIR, "Y_augmented.npy")
X_REAL_PATH       = os.path.join(BOOTSTRAP_DIR, "X_real.npy")
Y_REAL_PATH       = os.path.join(BOOTSTRAP_DIR, "Y_real.npy")
MODEL_OUT         = os.path.join(SCRIPT_DIR, "model.pkl")

N_BOOTSTRAP  = 500
NOISE_STD    = 0.05
RANDOM_SEED  = 42
TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def load_scores(score_file):
    wb = openpyxl.load_workbook(score_file)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    scores = {}
    for row in rows[1:]:
        if row[0] is None:
            continue
        key    = str(row[0]).strip()
        values = np.array([float(v) for v in row[1:6]], dtype=np.float32)
        scores[key] = values
    return scores


def impute_nans(X):
    col_means = np.nanmean(X, axis=0)
    col_means = np.where(np.isnan(col_means), 0.0, col_means)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])
    return X


def bootstrap_augment(X, Y, n_samples, noise_std, rng):
    n_orig = len(X)
    X_list = [X.copy()]
    Y_list = [Y.copy()]
    for _ in range(n_samples):
        idx    = rng.integers(0, n_orig)
        x_new  = X[idx].copy()
        y_new  = Y[idx].copy()
        x_new += rng.normal(0, noise_std * (np.abs(x_new) + 1e-6))
        if rng.random() < 0.5:
            idx2  = rng.integers(0, n_orig)
            alpha = rng.uniform(0.1, 0.9)
            x_new = alpha * x_new + (1 - alpha) * X[idx2]
            y_new = alpha * y_new + (1 - alpha) * Y[idx2]
        X_list.append(x_new.reshape(1, -1))
        Y_list.append(y_new.reshape(1, -1))
    return np.vstack(X_list), np.vstack(Y_list)


def build_mlp():
    return Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            activation="relu",
            solver="adam",
            alpha=0.01,
            learning_rate="adaptive",
            max_iter=2000,
            random_state=RANDOM_SEED,
            early_stopping=True,
            validation_fraction=0.15,
            n_iter_no_change=50,
            tol=1e-4,
        )),
    ])


# ─────────────────────────────────────────────
# STEP 1 — BOOTSTRAP AND SAVE DATA
# ─────────────────────────────────────────────
def step1_generate_and_save():
    print("\n" + "=" * 55)
    print("  STEP 1: Bootstrapping and saving data")
    print("=" * 55)

    rng    = np.random.default_rng(RANDOM_SEED)
    scores = load_scores(SCORE_FILE)

    X_list, Y_list = [], []
    for fname in sorted(os.listdir(DATA_SESSION_DIR)):
        if not fname.endswith(".csv"):
            continue
        key = fname.replace(".csv", "")
        if key not in scores:
            print(f"  [SKIP] No score for {key}")
            continue
        feats = extract_features(os.path.join(DATA_SESSION_DIR, fname))
        if feats is None or np.all(np.isnan(feats)):
            print(f"  [SKIP] Bad features for {key}")
            continue
        X_list.append(feats)
        Y_list.append(scores[key])
        print(f"  [OK]   {key}  features={feats.shape}  scores={scores[key]}")

    X_real = impute_nans(np.vstack(X_list))
    Y_real = np.vstack(Y_list)
    print(f"\n  Real data loaded: X={X_real.shape}, Y={Y_real.shape}")

    print(f"  Bootstrapping {N_BOOTSTRAP} synthetic samples...")
    X_aug, Y_aug = bootstrap_augment(X_real, Y_real, N_BOOTSTRAP, NOISE_STD, rng)
    X_aug = impute_nans(X_aug)
    print(f"  Augmented data : X={X_aug.shape}, Y={Y_aug.shape}")

    os.makedirs(BOOTSTRAP_DIR, exist_ok=True)
    np.save(X_AUG_PATH,  X_aug)
    np.save(Y_AUG_PATH,  Y_aug)
    np.save(X_REAL_PATH, X_real)
    np.save(Y_REAL_PATH, Y_real)

    print(f"\n  Saved to: {BOOTSTRAP_DIR}")
    print(f"    X_augmented.npy  -> shape {X_aug.shape}")
    print(f"    Y_augmented.npy  -> shape {Y_aug.shape}")
    print(f"    X_real.npy       -> shape {X_real.shape}")
    print(f"    Y_real.npy       -> shape {Y_real.shape}")
    print("  STEP 1 complete.")


# ─────────────────────────────────────────────
# STEP 2 — TRAIN MODEL FROM SAVED DATA
# ─────────────────────────────────────────────
def step2_train():
    print("\n" + "=" * 55)
    print("  STEP 2: Training MLP on saved bootstrapped data")
    print("=" * 55)

    X_aug  = np.load(X_AUG_PATH)
    Y_aug  = np.load(Y_AUG_PATH)
    print(f"\n  Loaded augmented data: X={X_aug.shape}, Y={Y_aug.shape}")

    # Normalise targets
    y_mean = Y_aug.mean(axis=0)
    y_std  = Y_aug.std(axis=0) + 1e-8
    Y_norm = (Y_aug - y_mean) / y_std

    # 5-fold CV
    print("\n  Running 5-fold cross-validation...")
    cv_model  = build_mlp()
    cv_scores = cross_val_score(cv_model, X_aug, Y_norm, cv=5, scoring="r2", n_jobs=-1)
    print(f"  CV R2 per fold : {cv_scores.round(4)}")
    print(f"  Mean CV R2     : {cv_scores.mean():.4f}  (+/-{cv_scores.std():.4f})")

    # Final fit
    print("\n  Fitting final model on all augmented data...")
    model = build_mlp()
    model.fit(X_aug, Y_norm)
    train_r2 = model.score(X_aug, Y_norm)
    print(f"  Train R2       : {train_r2:.4f}")

    # Save
    joblib.dump((model, y_mean, y_std), MODEL_OUT)
    print(f"\n  Model saved -> {MODEL_OUT}")
    print("  STEP 2 complete.")


# ─────────────────────────────────────────────
# STEP 3 — ACCURACY REPORT
# ─────────────────────────────────────────────
def step3_evaluate():
    print("\n" + "=" * 55)
    print("  STEP 3: Accuracy report")
    print("=" * 55)

    model, y_mean, y_std = joblib.load(MODEL_OUT)
    X_aug  = np.load(X_AUG_PATH)
    Y_aug  = np.load(Y_AUG_PATH)
    X_real = np.load(X_REAL_PATH)
    Y_real = np.load(Y_REAL_PATH)

    Y_aug_norm  = (Y_aug  - y_mean) / y_std
    Y_real_norm = (Y_real - y_mean) / y_std

    # ---- Augmented set ----
    aug_r2   = model.score(X_aug, Y_aug_norm)
    pred_aug = model.predict(X_aug) * y_std + y_mean
    aug_mae  = mean_absolute_error(Y_aug, pred_aug)

    print(f"\n  [Augmented set — {len(X_aug)} samples]")
    print(f"    R2  : {aug_r2:.4f}")
    print(f"    MAE : {aug_mae:.4f}")

    # ---- Real sessions ----
    real_r2   = model.score(X_real, Y_real_norm)
    pred_real = model.predict(X_real) * y_std + y_mean
    real_mae  = mean_absolute_error(Y_real, pred_real)

    print(f"\n  [Real sessions — {len(X_real)} samples]")
    print(f"    R2  : {real_r2:.4f}")
    print(f"    MAE : {real_mae:.4f}")

    # ---- Per-trait R2 ----
    print("\n  Per-trait R2 (real sessions):")
    for i, t in enumerate(TRAITS):
        tr2 = r2_score(Y_real[:, i], pred_real[:, i])
        print(f"    {t:<20} R2={tr2:+.4f}")

    # ---- Per-session table ----
    print("\n  Per-session predictions vs ground truth (real sessions):")
    col_hdr = "  " + f"{'Session':<12}" + "".join(f"  {t[:5]:>7}" for t in TRAITS)
    print(col_hdr)
    for i in range(len(X_real)):
        pred_row  = "  ".join(f"{v:7.2f}" for v in pred_real[i])
        truth_row = "  ".join(f"{v:7.2f}" for v in Y_real[i])
        print(f"  session_{i+1:<5}  pred : {pred_row}")
        print(f"               truth: {truth_row}")

    print("\n  STEP 3 complete.")
    print("=" * 55)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    step1_generate_and_save()
    step2_train()
    step3_evaluate()
