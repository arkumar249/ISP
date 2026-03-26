from build_dataset import build_dataset
import numpy as np

def debug_dataset(data_dir):
    print(" Building dataset...\n")

    X, Y = build_dataset(data_dir)

    print("\n BASIC INFO")
    print("Samples:", X.shape[0])
    print("Features:", X.shape[1])
    print("Targets:", Y.shape[1])

    print("\n SANITY CHECKS")

    # Check NaNs
    nan_count = np.isnan(X).sum()
    print("NaNs in X:", nan_count)

    if nan_count > 0:
        print(" Warning: NaNs still present!")

    # Check variance
    variances = np.var(X, axis=0)
    zero_var = np.sum(variances == 0)

    print("Zero-variance features:", zero_var)

    if zero_var > 0:
        print("Some features are constant → useless for ML")

    # Feature vs sample ratio
    print("\n FEATURE RATIO CHECK")

    if X.shape[1] > X.shape[0]:
        print("Too many features compared to samples!")
        print("Consider reducing features or collecting more data")

    elif X.shape[1] < 10:
        print("Too few features, model may underfit")

    else:
        print("Feature count looks reasonable")

    # Target check
    print("\n TARGET CHECK")
    print("Target mean:", np.mean(Y, axis=0))
    print("Target std:", np.std(Y, axis=0))

    if np.any(np.std(Y, axis=0) == 0):
        print("⚠️ Some targets have zero variance!")

    print("\n Debug complete.\n")

    return X, Y


if __name__ == "__main__":
    data_dir = "data"
    debug_dataset(data_dir)