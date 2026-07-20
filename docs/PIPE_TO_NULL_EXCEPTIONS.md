# Registry of `/dev/null` Output Redirection Exceptions

This document serves as the authoritative, audited registry of all permitted `/dev/null` stdout/stderr redirections within the `edge-ai` codebase.

---

## 📜 Operational Policy

Per **Rule 7** in [AI.md](file:///home/fekerr/src/edge-ai/AI.md):

1. **Strict Prohibition**: Piping or redirecting stdout/stderr to `/dev/null` (e.g. `> /dev/null`, `2> /dev/null`, `> /dev/null 2>&1`) is **prohibited by default**. Redirections hide error tracebacks, suppress critical diagnostic warnings, and make silent build/test failures hard to debug.
2. **Comment Requirement**: In the rare event that a `/dev/null` redirection is strictly necessary (e.g. checking command existence in shell scripts without emitting stdout noise), the line of code **MUST include an inline comment** explaining the necessity.
3. **Documentation Requirement**: Every approved `/dev/null` instance **MUST be registered in this document** with its file path, line number, rationale, and owner.
4. **Audit & Flagging**: Any un-commented or un-registered `/dev/null` usage discovered during repo audits must be flagged immediately and appended to [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md).

---

## 📋 Approved Exception Registry

| ID | File Path | Line Range | Purpose / Rationale | Status | Approved By |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `EXC-001` | `infra/make/base.mk` | L18 | Silent fallback on systems lacking `nproc` binary | Approved | fekerr / AGY |
| `EXC-002` | `infra/make/base.mk` | L19 | Suppress stderr when querying Linux sysfs P-core topology | Approved | fekerr / AGY |
| `EXC-003` | `infra/make/base.mk` | L20 | Suppress stderr when querying Linux sysfs E-core topology | Approved | fekerr / AGY |
| `EXC-004` | `infra/make/base.mk` | L23 | Suppress stderr when reading `/proc/meminfo` memory data | Approved | fekerr / AGY |
| `EXC-005` | `infra/make/base.mk` | L95 | Suppress output during `tree` command existence check | Approved | fekerr / AGY |
| `EXC-006` | `infra/make/litert.mk` | L33 | Suppress output during `bazel` build tool existence probe | Approved | fekerr / AGY |

---

## 🔍 Audit & Verification Procedure

To audit the repository for any un-registered `/dev/null` redirections, run:

```bash
grep -rn "/dev/null" . --exclude-dir={build,logs,.git,agy} --exclude="docs/PIPE_TO_NULL_EXCEPTIONS.md"
```

If any results are returned that are not listed in the table above, they must be audited, commented, logged in this registry, or appended to [TODO.md](file:///home/fekerr/src/edge-ai/TODO.md) for remediation.
