import pandas as pd
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "training_data.csv"
MODEL_PATH = BASE_DIR / "severity_model.joblib"

FEATURE_COLUMNS = [
    "has_compiler_warning",
    "has_array_bounds_warning",
    "has_output_mismatch",
    "has_crash",
    "has_inconsistent_return_code",
    "has_timeout",
    "num_compile_warnings",
    "num_runtime_failures",
]

TARGET_COLUMN = "severity_label"


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    print("=== Label Distribution ===")
    print(df["severity_label"].value_counts())
    print("==========================")

    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = DecisionTreeClassifier(max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, predictions, zero_division=0))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()