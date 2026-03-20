import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def write_test_log(log_path: Path, test_result: Dict[str, Any]) -> None:
    log_path.write_text(json.dumps(test_result, indent=2), encoding="utf-8")


def write_summary_report(report_path: Path, all_results: List[Dict[str, Any]]) -> None:
    total = len(all_results)
    failed = 0
    mismatch_count = 0
    compile_failures = 0
    runtime_failures = 0
    timeout_failures = 0

    lines = []
    lines.append("Compiler Behavior Testing Summary Report")
    lines.append(f"Generated at: {datetime.now().isoformat()}")
    lines.append("=" * 60)

    for result in all_results:
        test_name = result["test_name"]
        status = result["status"]

        if status != "PASSED":
            failed += 1
        if result["comparison"]["has_mismatch"]:
            mismatch_count += 1

        for opt, compile_result in result["compile_results"].items():
            if not compile_result["success"]:
                compile_failures += 1

        for opt, exec_result in result["execution_results"].items():
            if exec_result.get("timed_out"):
                timeout_failures += 1
            elif exec_result.get("returncode") not in (0, None):
                runtime_failures += 1

        lines.append(f"\nTest: {test_name}")
        lines.append(f"Status: {status}")

        for opt in result["compile_results"]:
            c = result["compile_results"][opt]
            e = result["execution_results"].get(opt, {})

            lines.append(
                f"  - {opt}: compile_success={c['success']}, "
                f"run_returncode={e.get('returncode')}, timed_out={e.get('timed_out', False)}"
            )

        lines.append(f"  - Output mismatch: {result['comparison']['has_mismatch']}")

        
        anomaly = result.get("anomaly", {})

        lines.append("  - Anomalies:")

        # Static
        static = anomaly.get("static", {})
        if static:
            lines.append("    Static:")
            for k, v in static.items():
                lines.append(f"      - {k}: {v}")

        # Runtime
        runtime = anomaly.get("runtime", [])
        if runtime:
            lines.append("    Runtime:")
            for r in runtime:
                lines.append(f"      - {r}")

        if not static and not runtime:
            lines.append("    None")

        lines.append(f"  - Severity: {anomaly.get('severity', 0)}")

        ml_prediction = result.get("ml_prediction", {})
        predicted_label = ml_prediction.get("predicted_severity_label")

        if predicted_label:
            lines.append(f"  - ML Predicted Severity: {predicted_label}")
        

    lines.append("\n" + "=" * 60)
    lines.append(f"Total tests: {total}")
    lines.append(f"Failed tests: {failed}")
    lines.append(f"Output mismatches: {mismatch_count}")
    lines.append(f"Compile failures: {compile_failures}")
    lines.append(f"Runtime failures: {runtime_failures}")
    lines.append(f"Timeout failures: {timeout_failures}")
   

    report_path.write_text("\n".join(lines), encoding="utf-8")