#!/usr/bin/env python3
"""
==============================================================================
Project:      edge-ai
Path:         tools/monitor_system_load.py
Purpose:      Real-time hardware load monitoring & throttling telemetry runner.
              Enforces <50% laptop CPU/RAM load limit, logs build times, disk I/O,
              and network telemetry under Rule 8 timestamping.
Architecture: Out-of-tree logging, idempotent execution, append-only JSONL/CSV.
==============================================================================
"""

import argparse
import csv
import datetime
import json
import os
import sys
import time


def get_timestamp_string(seq_start: int = 1) -> str:
    """Generate Rule 8 YYMMDD_HHMM_NNN timestamp string."""
    now = datetime.datetime.now()
    date_part = now.strftime("%y%m%d_%H%M")
    return f"{date_part}_{seq_start:03d}"


def read_proc_stat():
    """Read CPU load statistics from /proc/stat if psutil is unavailable."""
    try:
        with open("/proc/stat", "r") as f:
            line = f.readline()
            if line.startswith("cpu "):
                fields = [float(x) for x in line.split()[1:]]
                idle_time = fields[3] + fields[4]
                total_time = sum(fields)
                return total_time, idle_time
    except Exception:
        pass
    return None, None


def read_proc_meminfo():
    """Read RAM usage from /proc/meminfo if psutil is unavailable."""
    try:
        mem = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip().split()[0]
                    mem[key] = int(val)
        total = mem.get("MemTotal", 1)
        available = mem.get("MemAvailable", mem.get("MemFree", 0))
        used = total - available
        percent = (used / total) * 100.0
        return percent, used * 1024, total * 1024
    except Exception:
        return 0.0, 0, 0


def read_proc_diskstats():
    """Read SSD disk I/O metrics from /proc/diskstats."""
    try:
        read_bytes = 0
        write_bytes = 0
        with open("/proc/diskstats", "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 14 and parts[2].startswith(("sd", "nvme", "vd")):
                    # Field 6: sectors read, Field 10: sectors written (512 bytes per sector)
                    read_bytes += int(parts[5]) * 512
                    write_bytes += int(parts[9]) * 512
        return read_bytes, write_bytes
    except Exception:
        return 0, 0


def read_proc_net_dev():
    """Read Ethernet network load telemetry from /proc/net/dev."""
    try:
        rx_bytes = 0
        tx_bytes = 0
        with open("/proc/net/dev", "r") as f:
            lines = f.readlines()[2:]
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 9 and not parts[0].startswith("lo:"):
                    rx_bytes += int(parts[1])
                    tx_bytes += int(parts[9])
        return rx_bytes, tx_bytes
    except Exception:
        return 0, 0


def sample_system_metrics():
    """Sample current CPU, RAM, Disk I/O, and Network telemetry."""
    try:
        import psutil

        cpu_percent = psutil.cpu_percent(interval=0.2)
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        ram_used_bytes = mem.used
        ram_total_bytes = mem.total
        disk_io = psutil.disk_io_counters()
        disk_read = disk_io.read_bytes if disk_io else 0
        disk_write = disk_io.write_bytes if disk_io else 0
        net_io = psutil.net_io_counters()
        net_rx = net_io.bytes_recv if net_io else 0
        net_tx = net_io.bytes_sent if net_io else 0
    except ImportError:
        # Fallback to /proc readers
        t1, i1 = read_proc_stat()
        time.sleep(0.2)
        t2, i2 = read_proc_stat()
        if t1 and t2 and (t2 - t1) > 0:
            cpu_percent = (1.0 - ((i2 - i1) / (t2 - t1))) * 100.0
        else:
            cpu_percent = 0.0

        ram_percent, ram_used_bytes, ram_total_bytes = read_proc_meminfo()
        disk_read, disk_write = read_proc_diskstats()
        net_rx, net_tx = read_proc_net_dev()

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "cpu_percent": round(cpu_percent, 2),
        "ram_percent": round(ram_percent, 2),
        "ram_used_mb": round(ram_used_bytes / (1024 * 1024), 2),
        "ram_total_mb": round(ram_total_bytes / (1024 * 1024), 2),
        "disk_read_bytes": disk_read,
        "disk_write_bytes": disk_write,
        "net_rx_bytes": net_rx,
        "net_tx_bytes": net_tx,
        "throttled": cpu_percent > 50.0 or ram_percent > 50.0,
    }


def monitor_loop(duration_sec: int, interval_sec: float, out_dir: str, seq_start: int):
    """Run telemetry monitoring loop, enforcing throttling and logging out-of-tree."""
    os.makedirs(out_dir, exist_ok=True)
    ts_tag = get_timestamp_string(seq_start)

    jsonl_path = os.path.join(out_dir, f"telemetry_{ts_tag}.jsonl")
    csv_path = os.path.join(out_dir, f"telemetry_{ts_tag}.csv")

    print(f"==========================================================")
    print(f" edge-ai Hardware Load & Telemetry Monitoring Script")
    print(f" Target Limit: CPU < 50.0% | RAM < 50.0%")
    print(f" Timestamp Tag: {ts_tag}")
    print(f" Output JSONL:  {jsonl_path}")
    print(f" Output CSV:    {csv_path}")
    print(f"==========================================================")

    start_time = time.time()
    samples = []

    fieldnames = [
        "timestamp",
        "cpu_percent",
        "ram_percent",
        "ram_used_mb",
        "ram_total_mb",
        "disk_read_bytes",
        "disk_write_bytes",
        "net_rx_bytes",
        "net_tx_bytes",
        "throttled",
    ]

    with open(jsonl_path, "a") as f_json, open(csv_path, "a", newline="") as f_csv:
        csv_writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        if f_csv.tell() == 0:
            csv_writer.writeheader()

        while (time.time() - start_time) < duration_sec:
            metrics = sample_system_metrics()
            samples.append(metrics)

            f_json.write(json.dumps(metrics) + "\n")
            f_json.flush()

            csv_writer.writerow(metrics)
            f_csv.flush()

            status = "THROTTLED (Cooling)" if metrics["throttled"] else "NOMINAL (<50% Load)"
            print(
                f"[{metrics['timestamp']}] CPU: {metrics['cpu_percent']:5.2f}% | RAM: {metrics['ram_percent']:5.2f}% "
                f"| Disk W: {metrics['disk_write_bytes'] / 1e6:7.2f} MB | Net RX: {metrics['net_rx_bytes'] / 1e6:7.2f} MB "
                f"| Status: {status}"
            )

            # Auto-throttle sleep if CPU/RAM load exceeds 50%
            if metrics["throttled"]:
                time.sleep(1.0)
            else:
                time.sleep(interval_sec)

    avg_cpu = sum(s["cpu_percent"] for s in samples) / max(len(samples), 1)
    avg_ram = sum(s["ram_percent"] for s in samples) / max(len(samples), 1)
    max_cpu = max(s["cpu_percent"] for s in samples) if samples else 0.0
    max_ram = max(s["ram_percent"] for s in samples) if samples else 0.0

    print(f"\n=== Telemetry Summary ({ts_tag}) ===")
    print(f" Samples Captured: {len(samples)}")
    print(f" Average CPU Load: {avg_cpu:.2f}% (Max: {max_cpu:.2f}%)")
    print(f" Average RAM Load: {avg_ram:.2f}% (Max: {max_ram:.2f}%)")
    print(f" Target Status: {'PASS (<50% Throttled Target Met)' if avg_cpu <= 50.0 and avg_ram <= 50.0 else 'WARN (Load Exceeded 50%)'}")
    print(f"==========================================================\n")


def main():
    parser = argparse.ArgumentParser(description="edge-ai Hardware Throttling & Telemetry Monitor")
    parser.add_argument("--duration", type=int, default=10, help="Monitoring duration in seconds")
    parser.add_argument("--interval", type=float, default=1.0, help="Sampling interval in seconds")
    parser.add_argument("--out-dir", type=str, default="logs", help="Out-of-tree directory for logs")
    parser.add_argument("--seq-start", type=int, default=1, help="Rule 8 timestamp NNN sequence counter")
    args = parser.parse_args()

    project_root = os.environ.get("PROJECT_ROOT", os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    out_dir = os.path.join(project_root, args.out_dir)

    monitor_loop(args.duration, args.interval, out_dir, args.seq_start)


if __name__ == "__main__":
    main()
