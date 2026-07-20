# `edge-ai` Hardware Resource Throttling & Telemetry Specification (`RESOURCE_THROTTLING_AND_TELEMETRY.md`)

This document defines the operational rules and telemetry standards to ensure build and test matrices maintain laptop hardware utilization under **50%** ("cool & quiet execution principle: slow build is better than burning up hardware resources").

---

## ⚡ 1. Concise Hardware Throttling Rules (TL;DR)

1. **Max Job Concurrency**: Restrict parallel build jobs to `nproc / 2` or `make -j2` (never use `make -j` without limits).
2. **Process Priority (`nice` / `ionice`)**: Run all intensive compilation and benchmark loops with low process and I/O priority:
   ```bash
   nice -n 15 ionice -c 3 make build
   ```
3. **Thermal Guardrail**: If CPU temperature exceeds 70°C or CPU load exceeds 50%, pause background jobs for 10-15 seconds.
4. **Telemetry Metric Targets**:
   - **CPU Load**: `< 50%` total system load.
   - **Memory Usage**: `< 50%` total physical RAM.
   - **SSD I/O**: `< 50MB/s` sequential write rate.
   - **Ethernet / Network**: Throttled background artifact synchronization.

---

## 🏛️ 2. Verbose Telemetry Architecture

### A. Resource Metrics Monitored
When running out-of-tree builds (`build/`, `logs/`, `docs/`), the telemetry harness records:

| Telemetry Metric | Measurement Unit | Collection Method | Target Boundary |
| :--- | :--- | :--- | :--- |
| **Build Wall-Clock Time** | Seconds (`s`) | `/usr/bin/time -v` | Logged to `logs/build_time.log` |
| **CPU Utilization** | Percentage (`%`) | `top` / `/proc/stat` | `< 50%` |
| **RAM Consumption** | Megabytes (`MB`) | `/proc/meminfo` | `< 50%` total memory |
| **SSD Disk Load** | Read/Write (`MB/s`) | `/proc/diskstats` | Throttled write loops |
| **Ethernet / Network** | KB/s transferred | `/proc/net/dev` | Telemetry payload chunking |

### B. Telemetry Log Structure (`logs/hardware_telemetry.jsonl`)
```json
{
  "timestamp": "2026-07-20T08:40:00Z",
  "session_id": "260720_0834_001",
  "metrics": {
    "cpu_load_percent": 34.2,
    "ram_used_mb": 4096,
    "ram_total_mb": 16384,
    "ssd_write_mbps": 12.4,
    "net_kbps": 2.1
  },
  "status": "COOL_OK"
}
```
