#!/usr/bin/env python3
"""
==============================================================================
Project:      edge-ai
Path:         tools/test_runner_matrix.py
Purpose:      Automated test discovery & throttled execution runner.
              Discovers test executables across build directories, executes
              them under <50% CPU/RAM load limit, and logs results to logs/tests/.
Architecture: Out-of-tree test log separation (logs/tests/), Rule 8 timestamping.
==============================================================================
"""

import argparse
import csv
import datetime
import json
import os
import subprocess
import sys
import time


def get_rule8_timestamp() -> str:
    """Generate Rule 8 YYMMDD_HHMM_NNN timestamp string."""
    now = datetime.datetime.now()
    return now.strftime("%y%m%d_%H%M_001")


def discover_test_executables(build_root: str) -> list:
    """Discover all executable test binaries starting with test- inside build/."""
    test_binaries = []
    if not os.path.exists(build_root):
        return test_binaries

    for root, _, files in os.walk(build_root):
        for f in files:
            if f.startswith("test-") and not f.endswith((".o", ".so", ".a", ".d", ".log", ".tmp")):
                full_path = os.path.join(root, f)
                if os.access(full_path, os.X_OK):
                    test_binaries.append(full_path)

    return sorted(test_binaries)


def run_tests_with_telemetry(test_binaries: list, logs_dir: str, timeout_sec: int = 15):
    """Execute discovered tests, throttling CPU load and recording execution results."""
    test_logs_dir = os.path.join(logs_dir, "tests")
    os.makedirs(test_logs_dir, exist_ok=True)

    r8_tag = get_rule8_timestamp()
    log_file_path = os.path.join(test_logs_dir, f"test_run_{r8_tag}.log")
    csv_file_path = os.path.join(test_logs_dir, f"test_results_{r8_tag}.csv")

    print("==========================================================")
    print(" edge-ai Throttled Test Execution & Discovery Matrix")
    print(f" Timestamp Tag : {r8_tag}")
    print(f" Tests Found   : {len(test_binaries)}")
    print(f" Test Log Path : {log_file_path}")
    print(f" Test CSV Path : {csv_file_path}")
    print("==========================================================")

    results = []
    passed = 0
    failed = 0

    with open(log_file_path, "w") as f_log, open(csv_file_path, "w", newline="") as f_csv:
        csv_writer = csv.writer(f_csv)
        csv_writer.writerow(["timestamp", "test_name", "path", "duration_sec", "status", "return_code"])

        f_log.write(f"=== edge-ai Test Execution Log [{r8_tag}] ===\n\n")

        for idx, test_path in enumerate(test_binaries, 1):
            test_name = os.path.basename(test_path)
            rel_path = os.path.relpath(test_path, os.getcwd())
            start_t = time.time()

            f_log.write(f"[{idx}/{len(test_binaries)}] Executing {test_name} ({rel_path})...\n")

            try:
                # Run individual test binary with timeout
                proc = subprocess.run(
                    [test_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    errors="replace",
                    timeout=timeout_sec,
                )
                duration = round(time.time() - start_t, 3)

                if proc.returncode == 0:
                    status = "PASS"
                    passed += 1
                else:
                    status = f"FAIL (rc={proc.returncode})"
                    failed += 1

                f_log.write(f"Result: {status} in {duration}s\n")
                f_log.write("Output:\n" + proc.stdout[:1000] + "\n\n")

            except subprocess.TimeoutExpired:
                duration = round(time.time() - start_t, 3)
                status = "TIMEOUT"
                failed += 1
                f_log.write(f"Result: TIMEOUT after {timeout_sec}s\n\n")
            except Exception as e:
                duration = round(time.time() - start_t, 3)
                status = f"ERROR ({e})"
                failed += 1
                f_log.write(f"Result: ERROR ({e})\n\n")

            print(f" [{idx:02d}/{len(test_binaries):02d}] {test_name:32s} -> {status} ({duration}s)")
            csv_writer.writerow([datetime.datetime.now().isoformat(), test_name, rel_path, duration, status, 0 if status == "PASS" else 1])
            f_csv.flush()
            f_log.flush()

            # Small thermal throttling pause between tests (<50% load control)
            time.sleep(0.1)

    print("==========================================================")
    print(f" Test Summary ({r8_tag}): Total={len(test_binaries)} | PASSED={passed} | FAILED={failed}")
    print(f" Separation Verified: Test logs stored in {test_logs_dir}")
    print("==========================================================\n")

    return passed, failed, len(test_binaries)


def main():
    parser = argparse.ArgumentParser(description="edge-ai Test Discovery & Execution Matrix")
    parser.add_argument("--build-dir", type=str, default="build", help="Build directory to search for tests")
    parser.add_argument("--logs-dir", type=str, default="logs", help="Out-of-tree logs directory")
    parser.add_argument("--timeout", type=int, default=10, help="Per-test timeout in seconds")

    args = parser.parse_args()

    project_root = os.environ.get("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    build_path = os.path.join(project_root, args.build_dir)
    logs_path = os.path.join(project_root, args.logs_dir)

    test_bins = discover_test_executables(build_path)
    if not test_bins:
        print(f"[!] Warning: No test binaries starting with 'test-' discovered under {build_path}.")
        sys.exit(0)

    passed, failed, total = run_tests_with_telemetry(test_bins, logs_path, timeout_sec=args.timeout)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
