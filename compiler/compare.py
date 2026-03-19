from typing import Dict, Any


def compare_outputs(execution_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compare stdout across optimization levels.
    Marks mismatch if successful runs produce different outputs.
    """
    successful_outputs = {
        opt: result["stdout"]
        for opt, result in execution_results.items()
        if result.get("returncode") == 0 and not result.get("timed_out", False)
    }

    if len(successful_outputs) <= 1:
        return {
            "has_mismatch": False,
            "reference_output": next(iter(successful_outputs.values()), ""),
            "details": "Not enough successful runs to compare outputs.",
        }

    opts = list(successful_outputs.keys())
    reference_opt = opts[0]
    reference_output = successful_outputs[reference_opt]

    mismatches = []
    for opt, output in successful_outputs.items():
        if output != reference_output:
            mismatches.append(
                {
                    "optimization_level": opt,
                    "expected_from": reference_opt,
                    "expected_output": reference_output,
                    "actual_output": output,
                }
            )

    return {
        "has_mismatch": len(mismatches) > 0,
        "reference_output": reference_output,
        "details": mismatches if mismatches else "All successful outputs matched.",
    }