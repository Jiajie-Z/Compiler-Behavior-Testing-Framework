# Compiler Behavior Testing Framework

## Overview

This project is a lightweight **compiler validation and testing framework** designed to analyze how C programs behave under different compiler optimization levels.

It automates the full testing pipeline, including:

* Test discovery
* Compilation across multiple optimization levels (`-O0`, `-O2`, `-O3`)
* Execution and output capture
* Cross-optimization comparison
* Static (compile-time) and dynamic (runtime) anomaly detection
* Structured reporting with severity scoring

The framework is inspired by real-world **compiler QA and system validation workflows**, focusing on detecting undefined behavior and optimization-dependent inconsistencies.

---

## Key Features

### 1. Cross-Optimization Testing

Each test case is compiled and executed under multiple optimization levels:

* `-O0` (no optimization)
* `-O2` (standard optimization)
* `-O3` (aggressive optimization)

This enables detection of **optimization-dependent behavior differences**.

---

### 2. Static + Dynamic Analysis

The framework integrates both:

#### Static (Compile-Time) Signals

* Compiler warnings (e.g., `-Warray-bounds`)
* Detection of potential undefined behavior before execution

#### Dynamic (Runtime) Signals

* Crashes (non-zero return codes)
* Timeouts
* Output mismatches across optimization levels

---

### 3. AI-Driven Anomaly Detection

A rule-based anomaly detection module classifies issues into:

#### Static Anomalies

* `COMPILER_WARNING`
* `ARRAY_BOUNDS_WARNING`

#### Runtime Anomalies

* `CRASH_Ox`
* `OUTPUT_MISMATCH`
* `INCONSISTENT_RETURN_CODE`
* `TIMEOUT_Ox`

Each anomaly contributes to a **severity score**, helping prioritize issues.

---

### 4. Structured Reporting

Results are summarized in a human-readable report:

```
Test: out_of_bounds.c
Status: FAILED
  - O0: compile_success=True, run_returncode=0, timed_out=False
  - O2: compile_success=True, run_returncode=0, timed_out=False
  - O3: compile_success=True, run_returncode=0, timed_out=False
  - Output mismatch: True
  - Anomalies:
    Static:
      - COMPILER_WARNING: ['O0', 'O2', 'O3']
      - ARRAY_BOUNDS_WARNING: ['O0', 'O2', 'O3']
    Runtime:
      - OUTPUT_MISMATCH
  - Severity: 11
```

---

## Project Structure

```
.
├── run_tests.py              # Main test runner
├── detect_anomalies.py      # Anomaly detection logic
├── report.py                # Summary report generation
├── test_cases/
│   ├── basic/
│   │   ├── simple_math.c
│   │   ├── loop_test.c
│   │   └── ...
│   └── edge/
│       ├── null_pointer.c
│       ├── out_of_bounds.c
│       └── overflow_test.c
├── outputs/
│   ├── binaries/
│   ├── logs/
│   └── report.txt
```

---

## Example Test Cases

### Deterministic Cases (Expected to Pass)

* `simple_math.c`
* `loop_test.c`
* `branch_test.c`

These should produce consistent outputs across all optimization levels.

---

### Undefined Behavior Cases

#### 1. Null Pointer Dereference

* Crashes under `-O0`
* Behaves differently under optimized builds
* Detected as:

  * `CRASH_O0`
  * `OUTPUT_MISMATCH`
  * `INCONSISTENT_RETURN_CODE`

#### 2. Out-of-Bounds Access

* Does not crash
* Produces different outputs across optimization levels
* Compiler emits `-Warray-bounds`
* Detected as:

  * `ARRAY_BOUNDS_WARNING`
  * `OUTPUT_MISMATCH`

---

## How It Works

1. Discover all `.c` test files
2. Compile each file with:

   ```
   clang -O0 / -O2 / -O3
   ```
3. Execute each binary
4. Capture:

   * stdout / stderr
   * return codes
   * timeouts
5. Compare outputs across optimization levels
6. Detect anomalies
7. Generate structured report

---

## Installation & Setup

### Requirements

* Python 3.8+
* Clang installed and available in PATH

### Verify Clang

```bash
clang --version
```

---

## Running the Framework

```bash
py run_tests.py
```

Outputs:

* Per-test logs → `outputs/logs/`
* Summary report → `outputs/report.txt`

---

## Why This Project Matters

This project demonstrates key skills relevant to:

* Compiler QA
* GPU driver validation
* System-level testing
* Low-level debugging

### Key Insights

* Undefined behavior may not crash but still produce incorrect results
* Compiler optimizations can expose or mask bugs
* Static warnings + runtime behavior together provide stronger signals

---

## Resume Highlights

* Built a compiler validation framework to test C programs across optimization levels
* Integrated static compiler diagnostics with runtime anomaly detection
* Detected optimization-dependent undefined behavior, including crashes and silent output inconsistencies
* Designed a severity-based classification system to prioritize issues

---

## Future Improvements

* LLVM IR generation and diff analysis
* GCC vs Clang comparison
* HTML dashboard for visualization
* Fuzz testing integration
* More advanced anomaly classification (ML-based)

---

## License

MIT License
