from pathlib import Path
from typing import Dict, Any
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
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


def extract_features(test_result: Dict[str, Any]) -> Dict[str, int]:
    compile_results = test_result.get("compile_results", {})
    execution_results = test_result.get("execution_results", {})
    comparison = test_result.get("comparison", {})

    num_compile_warnings = 0
    has_compiler_warning = 0
    has_array_bounds_warning = 0

    for _, compile_result in compile_results.items():
        stderr = compile_result.get("stderr", "")
        if "warning:" in stderr:
            has_compiler_warning = 1
            num_compile_warnings += 1
        if "array-bounds" in stderr:
            has_array_bounds_warning = 1

    has_crash = 0
    has_timeout = 0
    num_runtime_failures = 0
    return_codes = set()

    for _, exec_result in execution_results.items():
        rc = exec_result.get("returncode")
        return_codes.add(rc)

        if rc not in (0, None):
            has_crash = 1
            num_runtime_failures += 1

        if exec_result.get("timed_out"):
            has_timeout = 1

    has_inconsistent_return_code = 1 if len(return_codes) > 1 else 0
    has_output_mismatch = 1 if comparison.get("has_mismatch", False) else 0

    return {
        "has_compiler_warning": has_compiler_warning,
        "has_array_bounds_warning": has_array_bounds_warning,
        "has_output_mismatch": has_output_mismatch,
        "has_crash": has_crash,
        "has_inconsistent_return_code": has_inconsistent_return_code,
        "has_timeout": has_timeout,
        "num_compile_warnings": num_compile_warnings,
        "num_runtime_failures": num_runtime_failures,
    }


def predict_severity_label(test_result: Dict[str, Any]) -> str:
    model = joblib.load(MODEL_PATH)
    features = extract_features(test_result)
    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    prediction = model.predict(df)[0]
    return str(prediction)