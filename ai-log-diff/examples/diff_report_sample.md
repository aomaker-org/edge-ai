# AI Semantic Log Diff Report

**Baseline Log A:** `ai-log-diff/examples/build_pass_001.log` (7 lines)  
**Target Log B:** `ai-log-diff/examples/build_fail_001.log` (7 lines)  
**Generated:** `2026-07-20T08:12:50.380435`  

---

## 📊 Diff Summary

| Metric | Count | Description |
| :--- | :--- | :--- |
| 🚨 **New Error Events** | `3` | Unexpected error/failure templates in Log B |
| ➕ **New Structural Events** | `3` | Templates appearing in Log B but not A |
| ➖ **Missing Events** | `3` | Templates present in Log A but omitted in B |
| 🔄 **Frequency Shift Events** | `0` | Events with count discrepancies |

---

## 🚨 New Error Cascades (Target Log B)

- `[x1]` `[<TIMESTAMP>] [error] [<ID>] Build aborted due to fatal compilation failure.`
- `[x1]` `[<TIMESTAMP>] [error] [<ID>] OpenVINO SDK header missing: intel_gpu_driver.h not found in include path`
- `[x1]` `[<TIMESTAMP>] [fatal] [<ID>] Compilation failed on target openvino_backend.cpp with exit code <N>.`

## ➕ Added Events (Target Log B)

- `[x1]` `[<TIMESTAMP>] [error] [<ID>] Build aborted due to fatal compilation failure.`
- `[x1]` `[<TIMESTAMP>] [error] [<ID>] OpenVINO SDK header missing: intel_gpu_driver.h not found in include path`
- `[x1]` `[<TIMESTAMP>] [fatal] [<ID>] Compilation failed on target openvino_backend.cpp with exit code <N>.`

## ➖ Missing Events (Omitted in Target Log B)

- `[was x1]` `[<TIMESTAMP>] [info] [<ID>] Build completed successfully with <N> errors and <N> warnings.`
- `[was x1]` `[<TIMESTAMP>] [info] [<ID>] Compiling src/engine/sycl_backend.cpp -> memory <HEX_ADDR>`
- `[was x1]` `[<TIMESTAMP>] [info] [<ID>] Linking target binary build/bin/edge-ai-engine`
