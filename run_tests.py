from pathlib import Path
from typing import Dict, Any, List

from config import (
    TEST_CASES_DIR,
    BINARIES_DIR,
    LOGS_DIR,
    REPORTS_DIR,
    OPTIMIZATION_LEVELS,
    EXECUTION_TIMEOUT_SECONDS,
    SUPPORTED_EXTENSIONS,
    ensure_directories,
)
from compiler.compile import compile_source
from compiler.execute import execute_binary
from compiler.compare import compare_outputs
from compiler.report import write_test_log, write_summary_report
from compiler.anomaly import detect_anomalies

from ml.predict_severity import predict_severity_label

def discover_test_cases(root_dir: Path) -> List[Path]:
    test_files = []
    for ext in SUPPORTED_EXTENSIONS:
        test_files.extend(root_dir.rglob(f"*{ext}"))
    return sorted(test_files)


def sanitize_name(path: Path) -> str:
    return path.stem.replace(" ", "_")


def run_single_test(source_file: Path) -> Dict[str, Any]:
    test_name = source_file.name
    test_stem = sanitize_name(source_file)

    compile_results: Dict[str, Any] = {}
    execution_results: Dict[str, Any] = {}

    for opt in OPTIMIZATION_LEVELS:
        binary_name = f"{test_stem}_{opt}"
        binary_path = BINARIES_DIR / binary_name

        compile_result = compile_source(source_file, binary_path, opt)
        compile_results[opt] = compile_result

        if compile_result["success"]:
            execution_result = execute_binary(binary_path, EXECUTION_TIMEOUT_SECONDS)
        else:
            execution_result = {
                "success": False,
                "stdout": "",
                "stderr": "Skipped execution due to compile failure.",
                "returncode": None,
                "timed_out": False,
            }

        execution_results[opt] = execution_result

    comparison = compare_outputs(execution_results)

    status = "PASSED"
    if comparison["has_mismatch"]:
        status = "FAILED"

    for opt in OPTIMIZATION_LEVELS:
        if not compile_results[opt]["success"]:
            status = "FAILED"
        if execution_results[opt]["timed_out"]:
            status = "FAILED"

    test_result = {
        "test_name": test_name,
        "source_file": str(source_file),
        "compile_results": compile_results,
        "execution_results": execution_results,
        "comparison": comparison,
        "status": status,
    }

    anomaly = detect_anomalies(test_result)

    print("ANOMALY:", anomaly) #debug

    test_result["anomaly"] = anomaly

    predicted_label = predict_severity_label(test_result)
    test_result["ml_prediction"] = {
    "predicted_severity_label": predicted_label}   

    if anomaly["severity"] >= 3:
        test_result["status"] = "FAILED"

    log_path = LOGS_DIR / f"{test_stem}.json"
    write_test_log(log_path, test_result)

    return test_result


def main() -> None:
    ensure_directories()

    test_cases = discover_test_cases(TEST_CASES_DIR)
    if not test_cases:
        print("No test cases found.")
        return

    print(f"Discovered {len(test_cases)} test case(s).")

    all_results = []
    for test_case in test_cases:
        print(f"Running: {test_case}")
        result = run_single_test(test_case)
        all_results.append(result)
        print(f"Finished: {result['test_name']} -> {result['status']}")

    summary_path = REPORTS_DIR / "summary_report.txt"
    write_summary_report(summary_path, all_results)

    print("\nDone.")
    print(f"Summary report written to: {summary_path}")


if __name__ == "__main__":
    main()