# Compiler Validation Framework with ML-Assisted Anomaly Detection

A system-level testing framework designed to detect undefined behavior and inconsistencies across compiler optimization levels, combining automated validation with ML-assisted anomaly classification.

---

## 🚀 Overview

This project implements an automated pipeline to validate compiler behavior by compiling and executing C programs under different optimization levels (`-O0`, `-O2`, `-O3`) and analyzing discrepancies.

It is designed to simulate real-world **compiler / system validation workflows**, similar to those used in low-level systems, GPU drivers, and compiler toolchains.

---

## 🔍 Motivation

Undefined behavior in C can lead to:

- Inconsistent outputs across optimization levels
- Silent correctness issues
- Crashes in some builds but not others

This framework systematically detects such issues and prioritizes them using both rule-based analysis and machine learning.

---

## ⚙️ Features

### 🔧 Multi-Optimization Testing
- Compile test cases with:
  - `-O0` (baseline)
  - `-O2` (optimized)
  - `-O3` (aggressive optimization)
- Compare runtime behavior across builds

---

### 🧪 Automated Execution Pipeline

[Test Cases]
↓
[Compile (Clang)]
↓
[Execute Binaries]
↓
[Output Comparison]
↓
[Anomaly Detection]
↓
[ML Severity Classification]
↓
[Report Generation]


---

### ⚠️ Rule-Based Anomaly Detection

#### Static Anomalies
- `COMPILER_WARNING`
- `ARRAY_BOUNDS_WARNING`

#### Runtime Anomalies
- `CRASH_Ox`
- `OUTPUT_MISMATCH`
- `INCONSISTENT_RETURN_CODE`
- `TIMEOUT_Ox`

Each anomaly contributes to a **severity score** for prioritization.

---

### 🤖 ML-Assisted Severity Classification

A Decision Tree model predicts severity levels:

- `LOW`
- `MEDIUM`
- `HIGH`

#### Input Features:
- Compiler warnings
- Array bounds warnings
- Output mismatches
- Crash / timeout signals
- Return code inconsistencies
- Runtime failure counts

---

### 📊 Structured Reporting

- Per-test detailed logs (JSON)
- Aggregated summary report
- Grouped anomaly output:
  - Static vs Runtime
- Severity scoring + ML prediction

---

## 🧠 Example Findings

| Test Case         | Issue Type                     | Insight |
|------------------|------------------------------|--------|
| `null_pointer.c` | Crash in `-O0` only          | UB leads to inconsistent runtime behavior |
| `out_of_bounds.c`| Different outputs across O2/O3| Memory access UB causes nondeterminism |

---

## 🏗️ Project Structure

```text
compiler-validation-framework/
│
├── test_cases/                # Input test programs
│   ├── basic/                 # Simple correctness tests
│   └── edge/                  # Undefined behavior cases (UB)
|   └── control_flow/          # Undefined behavior cases (UB)
│
├── outputs/                   # Generated artifacts
│   ├── binaries/              # Compiled executables
│   ├── logs/                  # Per-test JSON logs
│   └── reports/               # Summary reports
│
├── compiler/                  # Core pipeline modules
│   ├── compile.py             # Compilation logic (Clang wrapper)
│   ├── execute.py             # Execution with timeout handling
│   ├── compare.py             # Output comparison across builds
│   ├── anomaly.py             # Rule-based anomaly detection
│   └── report.py              # Report generation
│
├── ml/                        # ML-based severity classification
│   ├── generate_data.py       # Synthetic dataset generation
│   ├── train_model.py         # Model training (Decision Tree)
│   ├── predict_severity.py    # Inference logic
│   ├── model.pkl              # Trained model
│   └── training_data.csv      # Training dataset
│
├── config.py                  # Global configuration
├── run_tests.py               # Main entry point
└── README.md
---

## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

```

### 2. Train ML model
```bash
py ml/generate_data.py
py ml/train_model.py
```

### 3. Run test suite
```bash
py run_tests.py
```

### 4. View report
```
outputs/report.txt
```

---

## 🧩 Tech Stack

- Languages: Python, C
- Compiler: Clang
- Testing: PyTest-style automation pipeline
- ML: scikit-learn (Decision Tree)
- Data: JSON logging
- Tools: Git

---

## 🧠 Key Takeaways

- Compiler optimizations can expose undefined behavior in unexpected ways

- Cross-build validation is critical for system-level correctness

- Combining rule-based detection with ML improves issue prioritization

---

## 🔮 Future Improvements

- Integrate LLVM sanitizers (ASan / UBSan) in Linux/WSL environments
- Replace synthetic training data with real-world test logs
- Add fuzz testing for edge-case generation
- Extend ML model to anomaly classification
- Build visualization dashboards for analysis

---



## ✅ Status

- Functional
- ML-integrated
- Ready for portfolio and technical interviews
