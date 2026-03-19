def detect_anomalies(test_result):
    static_anomalies = {}
    runtime_anomalies = []
    severity = 0

    # ----------------------
    # 1. Compile-time (Static)
    # ----------------------
    for opt, compile_result in test_result["compile_results"].items():
        stderr = compile_result.get("stderr", "")

        if "warning:" in stderr:
            static_anomalies.setdefault("COMPILER_WARNING", []).append(opt)
            severity += 1

        if "array-bounds" in stderr:
            static_anomalies.setdefault("ARRAY_BOUNDS_WARNING", []).append(opt)
            severity += 2

    # ----------------------
    # 2. Runtime anomalies
    # ----------------------
    if test_result["comparison"]["has_mismatch"]:
        runtime_anomalies.append("OUTPUT_MISMATCH")
        severity += 2

    return_codes = set()

    for opt, exec_result in test_result["execution_results"].items():
        rc = exec_result.get("returncode")
        return_codes.add(rc)

        if rc not in (0, None):
            runtime_anomalies.append(f"CRASH_{opt}")
            severity += 3

        if exec_result.get("timed_out"):
            runtime_anomalies.append(f"TIMEOUT_{opt}")
            severity += 3

    if len(return_codes) > 1:
        runtime_anomalies.append("INCONSISTENT_RETURN_CODE")
        severity += 2

    return {
        "static": static_anomalies,
        "runtime": sorted(set(runtime_anomalies)),
        "severity": severity
    }