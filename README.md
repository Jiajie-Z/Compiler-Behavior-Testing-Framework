# Compiler Behavior Testing Framework with ML-Assisted Anomaly Detection

A lightweight compiler validation framework that detects undefined behavior and inconsistencies across optimization levels using rule-based analysis and ML-assisted severity classification.

---

## 🚀 Overview

This project implements an automated testing pipeline for validating compiler behavior by:

- Compiling C programs with multiple optimization levels (`-O0`, `-O2`, `-O3`)
- Executing binaries and comparing outputs
- Detecting anomalies caused by undefined behavior
- Classifying issue severity using rule-based logic and a machine learning model

It simulates real-world **compiler validation and system-level testing workflows**, similar to those used in GPU drivers, compilers, and low-level systems software.

---

## ⚙️ Features

### 🔧 Multi-Optimization Testing
- Compile test cases with:
  - `-O0` (no optimization)
  - `-O2` (standard optimization)
  - `-O3` (aggressive optimization)
- Compare runtime behavior across optimization levels

---

### 🧪 Automated Test Execution
- Batch execution of test cases
- Captures:
  - stdout / stderr
  - return codes
  - timeout behavior

---

### ⚠️ Rule-Based Anomaly Detection

Detects both **static** and **runtime anomalies**:

#### Static Anomalies
- `COMPILER_WARNING`
- `ARRAY_BOUNDS_WARNING`

#### Runtime Anomalies
- `CRASH_Ox`
- `OUTPUT_MISMATCH`
- `INCONSISTENT_RETURN_CODE`
- `TIMEOUT_Ox`

Each anomaly contributes to a **severity score**, enabling prioritization of issues.

---

### 🤖 ML-Assisted Severity Classification

A lightweight machine learning model predicts issue severity based on extracted features.

#### Features used:
- Compiler warnings
- Array bounds warnings
- Output mismatches
- Crashes / timeouts
- Return code inconsistencies
- Runtime failure counts

#### Model:
- Decision Tree Classifier (`scikit-learn`)
- Trained on synthetic labeled data

> ML predictions are used as an auxiliary signal to complement rule-based detection.

---

## 📊 Example Output

```
Test: null_pointer.c
Status: FAILED

  - O0: compile_success=True, run_returncode=3221225477
  - O2: compile_success=True, run_returncode=0
  - O3: compile_success=True, run_returncode=0

  - Output mismatch: True

  - Anomalies:
    Runtime:
      - CRASH_O0
      - INCONSISTENT_RETURN_CODE
      - OUTPUT_MISMATCH

  - Severity: 7
  - ML Predicted Severity: HIGH
```

---

## 🧠 Key Insight

This framework highlights how **undefined behavior in C** can lead to:

- Different outputs across optimization levels
- Crashes in one optimization level but not others
- Silent correctness issues

Example cases:
- `null_pointer.c` → crash in `-O0`, but not in optimized builds
- `out_of_bounds.c` → inconsistent outputs across optimization levels

---

## 🏗️ Project Structure

```
.
├── test_cases/
│   ├── basic/
│   └── edge/
│
├── outputs/
│   ├── binaries/
│   ├── logs/
│   └── report.txt
│
├── ml/
│   ├── generate_data.py
│   ├── train_model.py
│   ├── predict_severity.py
│   ├── model.pkl
│   └── training_data.csv
│
├── run_tests.py
├── report.py
└── README.md
```

---

## ▶️ How to Run

### 1. Generate ML training data
```bash
py ml/generate_data.py
```

### 2. Train the model
```bash
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

## 🧩 Technologies Used

- Python (automation framework)
- C / Clang (compiler testing)
- scikit-learn (ML model)
- JSON (logging & reporting)

---

## 🎯 Why This Project Matters

This project demonstrates:

- Compiler behavior validation
- Undefined behavior detection
- Cross-optimization testing
- System-level debugging workflows
- Integration of rule-based and ML-based validation

It is particularly relevant to:

- Compiler testing
- Low-level systems software QA
- Performance and correctness testing

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
