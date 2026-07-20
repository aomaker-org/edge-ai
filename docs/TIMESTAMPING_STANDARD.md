# Timestamping Standard & Sequence Counter Specification (`docs/TIMESTAMPING_STANDARD.md`)

This document defines the authoritative timestamping specification for the `edge-ai` project. All automated tooling, log generators, artifact archiving scripts, and AI/human agents MUST adhere to this standard.

---

## 🏛️ 1. Canonical Timestamp Format

The standard timestamp format for `edge-ai` is:

$$\text{\texttt{YYMMDD\_HHMM\_NNN}}$$

*(Or the 4-digit year variant: $\text{\texttt{YYYYMMDD\_HHMM\_NNN}}$)*

### Format Breakdown

| Segment | Length | Format / Description | Example |
| :--- | :--- | :--- | :--- |
| **`YYMMDD`** | 6 chars | 2-digit Year, 2-digit Month, 2-digit Day | `260720` (July 20, 2026) |
| **`HHMM`** | 4 chars | 24-hour Hour and Minute (0000–2359) | `0805` (08:05 AM) |
| **`NNN`** | 3 chars | Zero-padded 3-digit sequence counter (`001`–`999`) | `001` |

**Full Example:** `260720_0805_001`

---

## ⚖️ 2. Architectural Rationale & Best Practice Challenges

### Why `YYMMDD_HHMM_NNN` over raw ISO-8601 (`2026-07-20T08:05:54Z`)?

1. **Filesystem Safety**: Standard ISO-8601 contains colons (`:`), which are **illegal characters** on Windows NTFS/FAT filesystems and can break cross-platform shell scripts between WSL2, Linux, and Windows 11 host environments.
2. **Lexicographical Sortability**: Strings formatted as `YYMMDD_HHMM_NNN` sort naturally in chronological order using standard string comparison (`ls -1`, `sort`).
3. **Collision Resistance (`NNN`)**: In fast automated build loops or multi-agent execution sessions, multiple events can occur within the same minute (`HHMM`). The 3-digit `NNN` sequence counter guarantees uniqueness and strict ordinal sequence.

### 💡 Best Practice Challenge: 4-Digit Year (`YYYYMMDD`) Recommendation
While `260720_HHMM_NNN` (6-digit date) is supported as requested, **4-digit year prefixes (`20260720_HHMM_NNN`) are recommended** when interacting with long-term external archives or multi-decade log analysis tools to prevent century ambiguity.

---

## 🔄 3. Sequence Counter (`NNN`) Lifecycle & Reset Rules

1. **Auto-Increment**: `NNN` starts at `001` for the first event within a given minute/session and increments sequentially (`001`, `002`, `003`...) for each subsequent timestamped asset generated.
2. **Auto-Reset**: `NNN` automatically resets to `001` when:
   - The date (`YYMMDD`) or time block changes.
   - A new major build or test session is initialized.
3. **Human Agent Override**: A human maintainer may explicitly instruct agents or tooling to reset or override the sequence counter (e.g. *"Start sequence at 001 for this task"*).
4. **Collision Handling**: If a target file already exists with sequence `NNN`, the counter must automatically increment to `NNN+1` (`002`) to preserve append-only idempotency without overwriting existing assets.

---

## 📌 4. Application Contexts

| Context | Application Example | Description |
| :--- | :--- | :--- |
| **AGY Session Logs** | `agy/sessions/260720_0805_001_session.md` | Session markdown records captured in `agy/` |
| **Build & Test Logs** | `logs/builds/260720_0805_001_openvino.log` | Ephemeral build logs in `logs/` |
| **Artifact Archives** | `260720_0805_001_core12_telemetry.zip` | Archived telemetry snapshots |
| **Ledger Entries (`TODO.md`)** | `- 260720_0805_001 - Enforced Rule 8...` | Timestamped log entries in `TODO.md` |
| **Git Commit Tagging** | `[260720_0805_001] Add timestamping standard` | Optional commit message prefix for major milestones |

---

## 🛠️ 5. Utility Implementation Reference

A Python helper or shell utility can generate compliance timestamps using:

```python
from datetime import datetime

def generate_timestamp(sequence: int = 1, use_four_digit_year: bool = False) -> str:
    now = datetime.now()
    date_str = now.strftime("%Y%m%d" if use_four_digit_year else "%y%m%d")
    time_str = now.strftime("%H%M")
    seq_str = f"{sequence:03d}"
    return f"{date_str}_{time_str}_{seq_str}"
```
