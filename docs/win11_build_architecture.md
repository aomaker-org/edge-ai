# Windows 11 Build Architecture & Design Critique

> **Project:** `edge-ai`  
> **Author:** fekerr & Antigravity  
> **Date:** July 20, 2026  
> **Status:** Active Architectural Standard  

---

## 1. Overview & Problem Statement

Building complex C++/AI projects on Windows 11 across multiple backends (MSVC 2022, Intel oneAPI / SYCL, OpenVINO, OpenSSL, Python/uv) historically relies on launch-time environment chaining. 

In projects like `irislime`, environment configuration was initiated by Windows Terminal profiles chaining multiple batch files together inside a single `commandline` string:

```json
"commandline": "cmd.exe /s /c \"\"C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\Common7\\Tools\\VsDevCmd.bat\" -arch=amd64 && \"C:\\Program Files (x86)\\Intel\\oneAPI\\setvars.bat\" && \"C:\\Program Files\\Git\\bin\\bash.exe\" --login -i\""
```

While functional, this pattern introduces significant brittleness and maintenance overhead. This document provides a formal critique of terminal-chained environment loading and establishes the design principles behind `edge-ai`'s deterministic, multi-shell build environment architecture.

---

## 2. Critique of Terminal-Chained Profile Execution

### ❌ 1. Terminal Profile Coupling (Lack of Portability)
Chaining environment batch files inside Windows Terminal `settings.json` couples project build readiness to a specific terminal emulator configuration. 
- **CI/CD Failure:** CI runners (GitHub Actions, Azure Pipelines), VS Code integrated terminals, Rider/CLion subshells, or bare PowerShell windows fail to build because they do not execute Windows Terminal's profile `commandline` string.
- **Escape Syntax Complexity:** Escalating quotes inside `cmd.exe /s /c ""` strings easily breaks across different Windows Terminal schema versions or copy-paste transfers.

### ❌ 2. Subshell Process Nesting & Startup Latency
Launching a chained profile spawns a deep process hierarchy:
$$\text{WindowsTerminal.exe} \longrightarrow \text{cmd.exe} \longrightarrow \text{VsDevCmd.bat} \longrightarrow \text{setvars.bat} \longrightarrow \text{bash.exe}$$
- **Startup Overhead:** Each stage parses batch files, runs `wmic`/`vswhere` queries, and spawns sub-processes, resulting in 1.5s - 3.0s startup latency per terminal tab.
- **Swallowed Error Exit Codes:** If `VsDevCmd.bat` or `setvars.bat` fails due to a missing component, `cmd.exe` still executes the final `&& bash.exe` command, leaving the shell in a silently broken state where compiler binaries are missing.

### ❌ 3. Path Translation Artifacts in Git Bash (MSYS2 Path Conversion)
Git for Windows wraps MSYS2's POSIX path translation logic.
- **Path Distortion:** Command-line options starting with slashes (e.g. MSVC compiler flags like `/MP`, `/utf-8`, `/std:c++17`, or CMake build flags `/p:Configuration=Release`) are incorrectly intercepted by Git Bash and converted into Windows file paths (e.g. `C:\Program Files\Git\MP`).
- **Fix Required:** Git Bash users must set `export MSYS_NO_PATHCONV=1` when calling MSVC or Windows native binaries (`cl.exe`, `msbuild.exe`).

---

## 3. The `edge-ai` Solution: Deterministic Environment Capture

To eliminate profile brittleness, `edge-ai` introduces **In-Shell Deterministic Capture** via [`infra/win11/capture_env.py`](file:///C:/Users/feker/src/edge-ai/infra/win11/capture_env.py).

```
                      ┌────────────────────────────┐
                      │   VsDevCmd.bat -arch=amd64 │
                      └─────────────┬──────────────┘
                                    │
                                    ▼
                      ┌────────────────────────────┐
                      │   Intel oneAPI setvars.bat │
                      └─────────────┬──────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │  capture_env.py (Computes Env Delta) │
                 └──────────────────┬───────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                          ▼                          ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│ .edgeai_env.ps1 │        │ .edgeai_env.sh  │        │ .edgeai_env.bat │
│  (PowerShell 7) │        │   (Git Bash)    │        │    (CMD Batch)  │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

### Key Advantages:
1. **Instant Loading (< 10ms):** Sourcing pre-captured environment scripts sets process variables directly in memory without re-running VS/Intel detection scripts every time a tab opens.
2. **Universal Shell Support:** Identical environment states are loaded regardless of whether the developer uses PowerShell 7, Git Bash, or CMD.
3. **Automatic Fallback:** `config_win11_ps7.ps1`, `config_win11_bash`, and `config_win11_bat.bat` automatically trigger `capture_env.py` if `cl.exe` is missing from session memory.

---

## 4. Shell Architecture Comparison

| Feature | PowerShell 7 (`config_win11_ps7`) | Git Bash (`config_win11_bash`) | CMD Batch (`config_win11_bat`) |
| :--- | :--- | :--- | :--- |
| **Native Windows Support** | First-Class | Emulated (MSYS2 Layer) | Legacy First-Class |
| **Path Handling** | Windows (`C:\...`) | POSIX (`/c/...`) | Windows (`C:\...`) |
| **Build Functions** | Native PS Cmdlets | Bash Functions | DOSKEY Aliases |
| **Path Conversion Risks**| None | High (`MSYS_NO_PATHCONV`) | None |
| **Object Pipeline** | Yes | Text Stream Only | Text Stream Only |
| **Performance** | Fast | Moderate | Fast |

> [!RECOMMENDATION]
> **Primary Shell:** PowerShell 7 (`pwsh.exe`) is recommended for native C++ development on Windows 11 due to zero path translation friction and native integration with `vswhere` and `winget`.

---

## 5. CMakePresets.json vs Shell Environment Variables

While shell loader scripts (`config_win11_*`) set up session variables, modern C++ best practice favors offloading build toolchain details to **CMake Presets** ([`CMakePresets.json`](file:///C:/Users/feker/src/edge-ai/CMakePresets.json)).

### Architectural Best Practices:
1. **Use `CMakePresets.json` for Compiler & Generator Settings:** Define generators (`Ninja`), architecture (`x64`), and build types inside `CMakePresets.json` rather than hardcoding them in shell scripts.
2. **Keep Environment Loaders Focused on SDK Paths:** Limit `config_win11_*` scripts to declaring external SDK locations (`INTEL_OPENVINO_DIR`, `OPENSSL_ROOT_DIR`, `ONEAPI_ROOT`).
3. **Isolate Runtime DLL Directories:** Ensure runtime DLL paths (`OpenVINO`, `OpenSSL`) are appended to `PATH` in environment scripts to prevent `0xC0000135` (DLL Not Found) runtime execution failures.

---

## 6. Verification & Verification Matrix

To verify build environment integrity on a fresh Windows 11 machine:

```powershell
# 1. Run Provisioner & Audit
. .\provision_win11.ps1 -InstallMissing -GenerateEnvSnapshot

# 2. Source PowerShell 7 Environment
. .\config_win11_ps7.ps1

# 3. Verify System Status
show_edgeai_status

# 4. Configure & Build via CMake Preset
edgeai_cmake win11-msvc-release
edgeai_build win11-msvc-release
```
