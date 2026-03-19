import subprocess
from pathlib import Path
from typing import Dict, Any


def execute_binary(binary_path: Path, timeout_seconds: int) -> Dict[str, Any]:
    """
    Execute a compiled binary and capture stdout, stderr, and return code.
    """
    try:
        result = subprocess.run(
            [str(binary_path)],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "success": False,
            "stdout": exc.stdout or "",
            "stderr": (exc.stderr or "") + "\nExecution timed out.",
            "returncode": None,
            "timed_out": True,
        }
    except Exception as exc:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Execution failed: {exc}",
            "returncode": -1,
            "timed_out": False,
        }