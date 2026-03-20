import csv
import random

OUTPUT_FILE = "ml/training_data.csv"

def generate_sample():
    has_compiler_warning = random.randint(0, 1)
    has_array_bounds_warning = random.randint(0, 1)
    has_output_mismatch = random.randint(0, 1)
    has_crash = random.randint(0, 1)
    has_inconsistent_return_code = random.randint(0, 1)
    has_timeout = random.randint(0, 1)

    # 让一些组合更合理
    if has_crash:
        has_timeout = random.randint(0, 1)

    num_compile_warnings = 0
    if has_compiler_warning:
        num_compile_warnings = random.randint(1, 3)

    if has_array_bounds_warning and not has_compiler_warning:
        has_compiler_warning = 1
        if num_compile_warnings == 0:
            num_compile_warnings = random.randint(1, 3)

    num_runtime_failures = 1 if has_crash else 0

    # 标签规则：保证 LOW 存在
    if has_crash or has_timeout:
        label = "HIGH"
    elif (
        has_output_mismatch
        or has_inconsistent_return_code
        or has_compiler_warning
        or has_array_bounds_warning
    ):
        label = "MEDIUM"
    else:
        label = "LOW"

    return [
        has_compiler_warning,
        has_array_bounds_warning,
        has_output_mismatch,
        has_crash,
        has_inconsistent_return_code,
        has_timeout,
        num_compile_warnings,
        num_runtime_failures,
        label,
    ]


def main():
    rows = []

    # 先强制加一些 LOW 样本
    for _ in range(15):
        rows.append([0, 0, 0, 0, 0, 0, 0, 0, "LOW"])

    # 再加一些 MEDIUM 样本
    for _ in range(15):
        rows.append([
            1,                              # has_compiler_warning
            random.randint(0, 1),          # has_array_bounds_warning
            random.randint(0, 1),          # has_output_mismatch
            0,                              # has_crash
            random.randint(0, 1),          # has_inconsistent_return_code
            0,                              # has_timeout
            random.randint(1, 3),          # num_compile_warnings
            0,                              # num_runtime_failures
            "MEDIUM"
        ])

    # 再加一些 HIGH 样本
    for _ in range(15):
        rows.append([
            random.randint(0, 1),
            random.randint(0, 1),
            random.randint(0, 1),
            1,                              # has_crash
            random.randint(0, 1),
            random.randint(0, 1),
            random.randint(0, 3),
            1,                              # num_runtime_failures
            "HIGH"
        ])

    # 再补一些随机样本
    for _ in range(20):
        rows.append(generate_sample())

    random.shuffle(rows)

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "has_compiler_warning",
            "has_array_bounds_warning",
            "has_output_mismatch",
            "has_crash",
            "has_inconsistent_return_code",
            "has_timeout",
            "num_compile_warnings",
            "num_runtime_failures",
            "severity_label"
        ])
        writer.writerows(rows)

    print("Generated dataset!")


if __name__ == "__main__":
    main()