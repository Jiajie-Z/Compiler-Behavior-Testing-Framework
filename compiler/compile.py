import subprocess
from pathlib import Path
from typing import Dict, Any

from config import COMPILER, C_STANDARD


def compile_source(source_file: Path, output_binary: Path, optimization_level: str) -> Dict[str, Any]:
    """
    Compile a C source file using clang.
    Returns a dict containing success flag, command, stdout, stderr, and return code.
    """
    cmd = [
        COMPILER,
        f"-{optimization_level}",
        f"-std={C_STANDARD}",
        str(source_file),
        "-o",
        str(output_binary),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "success": result.returncode == 0,
            "command": " ".join(cmd),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "binary_path": str(output_binary),
        }
    except FileNotFoundError:
        return {
            "success": False,
            "command": " ".join(cmd),
            "stdout": "",
            "stderr": f"Compiler '{COMPILER}' not found. Please install clang and ensure it is in PATH.",
            "returncode": -1,
            "binary_path": str(output_binary),
        }