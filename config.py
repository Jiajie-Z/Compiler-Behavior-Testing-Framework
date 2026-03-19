from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

TEST_CASES_DIR = BASE_DIR / "test_cases"
OUTPUT_DIR = BASE_DIR / "outputs"
BINARIES_DIR = OUTPUT_DIR / "binaries"
LOGS_DIR = OUTPUT_DIR / "logs"
REPORTS_DIR = OUTPUT_DIR / "reports"

COMPILER = "clang"
C_STANDARD = "c11"
OPTIMIZATION_LEVELS = ["O0", "O2", "O3"]

EXECUTION_TIMEOUT_SECONDS = 3

SUPPORTED_EXTENSIONS = [".c"]

def ensure_directories() -> None:
    BINARIES_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)