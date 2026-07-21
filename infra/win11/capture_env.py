#!/usr/bin/env python3
"""
==============================================================================
Filename:     infra/win11/capture_env.py
Purpose:      Deterministic Windows Build Environment Capturer for edge-ai
Type:         Executed (Python 3 script)
Attribution:  fekerr & Antigravity (20260720 / Native Win11 Integration)
==============================================================================

Description:
  Executes chained Windows batch scripts (e.g. VsDevCmd.bat, setvars.bat) 
  inside cmd.exe and captures the environment variables present at each stage.
  
  Exports snapshots into multiple formats (.json, .ps1, .sh, .bat) to enable
  less brittle, deterministic environment sourcing across PowerShell 7, 
  Git Bash, and CMD without relying on Windows Terminal profile chaining.

Usage:
  python infra/win11/capture_env.py [--vs-arch amd64] [--output-dir .] [--verbose]
==============================================================================
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

def parse_args():
    parser = argparse.ArgumentParser(description="Capture chained batch file environment variables.")
    parser.add_argument("--vs-arch", default="amd64", help="Architecture for VsDevCmd.bat (e.g., amd64, x86, arm64)")
    parser.add_argument("--vs-path", default=None, help="Explicit path to VsDevCmd.bat")
    parser.add_argument("--oneapi-path", default=None, help="Explicit path to Intel oneAPI setvars.bat")
    parser.add_argument("--output-dir", default=None, help="Directory to output environment files (default: PROJECT_ROOT)")
    parser.add_argument("--verbose", action="store_true", help="Print verbose environment deltas")
    return parser.parse_args()

def find_vswhere() -> Path | None:
    program_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
    vswhere_path = Path(program_files_x86) / "Microsoft Visual Studio" / "Installer" / "vswhere.exe"
    if vswhere_path.exists():
        return vswhere_path
    return None

def locate_vsdevcmd() -> Path | None:
    vswhere = find_vswhere()
    if vswhere:
        try:
            res = subprocess.run(
                [str(vswhere), "-latest", "-products", "*", "-requires", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64", "-property", "installationPath"],
                capture_output=True, text=True, check=True
            )
            install_path = res.stdout.strip()
            if install_path:
                candidate = Path(install_path) / "Common7" / "Tools" / "VsDevCmd.bat"
                if candidate.exists():
                    return candidate
        except Exception:
            pass

    candidates = [
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\Tools\VsDevCmd.bat"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\Tools\VsDevCmd.bat"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\Enterprise\Common7\Tools\VsDevCmd.bat"),
        Path(r"C:\Program Files\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat"),
        Path(r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\Common7\Tools\VsDevCmd.bat"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def locate_oneapi_setvars() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Intel\oneAPI\setvars.bat"),
        Path(r"C:\Program Files\Intel\oneAPI\setvars.bat"),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def dump_cmd_env(command_chain: str) -> Dict[str, str]:
    full_cmd = f'cmd.exe /s /c "{command_chain} && set"'
    res = subprocess.run(full_cmd, capture_output=True, text=True, shell=True)
    if res.returncode != 0:
        print(f"[!] Warning: Batch execution returned code {res.returncode}", file=sys.stderr)
        if res.stderr:
            print(f"    Stderr: {res.stderr.strip()}", file=sys.stderr)

    env_dict = {}
    for line in res.stdout.splitlines():
        line = line.strip()
        if "=" in line:
            parts = line.split("=", 1)
            env_dict[parts[0]] = parts[1]
    return env_dict

def compute_deltas(base_env: Dict[str, str], stage_env: Dict[str, str]) -> Dict[str, str]:
    deltas = {}
    base_lower = {k.lower(): (k, v) for k, v in base_env.items()}
    for k, v in stage_env.items():
        k_lower = k.lower()
        if k_lower not in base_lower or base_lower[k_lower][1] != v:
            deltas[k] = v
    return deltas

def main():
    args = parse_args()
    
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else project_root

    print("==================================================================")
    print(" edge-ai Windows Environment Capture Utility")
    print(f" Project Root: {project_root}")
    print(f" Output Dir:   {output_dir}")
    print("==================================================================")

    base_env = dict(os.environ)

    vsdevcmd = Path(args.vs_path) if args.vs_path else locate_vsdevcmd()
    oneapi_setvars = Path(args.oneapi_path) if args.oneapi_path else locate_oneapi_setvars()

    print(f"[*] Visual Studio DevCmd: {vsdevcmd if vsdevcmd else 'NOT FOUND'}")
    print(f"[*] Intel oneAPI setvars: {oneapi_setvars if oneapi_setvars else 'NOT FOUND (Optional)'}")

    stages = []
    stages.append(("Stage 0: Initial Shell", base_env))

    cmd_stage1 = ""
    if vsdevcmd and vsdevcmd.exists():
        cmd_stage1 = f'"{vsdevcmd}" -arch={args.vs_arch}'
        print(f"[*] Capturing Stage 1 (Visual Studio {args.vs_arch})...")
        env_stage1 = dump_cmd_env(cmd_stage1)
        stages.append(("Stage 1: VS2022 DevCmd", env_stage1))
    else:
        print("[!] Visual Studio VsDevCmd.bat not found; skipping VS capture stage.")
        env_stage1 = base_env

    if oneapi_setvars and oneapi_setvars.exists():
        cmd_stage2 = f'{cmd_stage1} && "{oneapi_setvars}"' if cmd_stage1 else f'"{oneapi_setvars}"'
        print("[*] Capturing Stage 2 (VS2022 + Intel oneAPI)...")
        env_stage2 = dump_cmd_env(cmd_stage2)
        stages.append(("Stage 2: VS2022 + oneAPI", env_stage2))
    else:
        print("[i] Intel oneAPI setvars.bat not found or skipped.")
        env_stage2 = env_stage1

    final_env = stages[-1][1]
    deltas = compute_deltas(base_env, final_env)

    print(f"\n[+] Total environment variables added/modified across stages: {len(deltas)}")
    if args.verbose:
        for k, v in sorted(deltas.items()):
            print(f"    {k} = {v[:80]}..." if len(v) > 80 else f"    {k} = {v}")

    json_path = output_dir / ".edgeai_env.json"
    ps1_path = output_dir / ".edgeai_env.ps1"
    sh_path = output_dir / ".edgeai_env.sh"
    bat_path = output_dir / ".edgeai_env.bat"

    export_payload = {
        "metadata": {
            "vsdevcmd": str(vsdevcmd) if vsdevcmd else None,
            "vs_arch": args.vs_arch,
            "oneapi_setvars": str(oneapi_setvars) if oneapi_setvars else None,
            "captured_variables_count": len(deltas),
        },
        "deltas": deltas,
        "full_environment": final_env
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)
    print(f"[+] Exported JSON snapshot: {json_path}")

    with open(ps1_path, "w", encoding="utf-8") as f:
        f.write("# Auto-generated PowerShell environment snapshot for edge-ai\n")
        f.write(f"# Captured from: {vsdevcmd}\n\n")
        for k, v in sorted(deltas.items()):
            v_escaped = v.replace('`', '``').replace('$', '`$').replace('"', '`"')
            f.write(f'$env:{k} = "{v_escaped}"\n')
    print(f"[+] Exported PowerShell 7 script: {ps1_path}")

    with open(sh_path, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env bash\n")
        f.write("# Auto-generated Bash environment snapshot for edge-ai\n")
        f.write(f"# Captured from: {vsdevcmd}\n\n")
        for k, v in sorted(deltas.items()):
            v_escaped = v.replace('\\', '/').replace('"', '\\"') if k.upper() in ("PATH", "INCLUDE", "LIB", "LIBPATH") else v.replace('"', '\\"')
            f.write(f'export {k}="{v_escaped}"\n')
    print(f"[+] Exported Git Bash script: {sh_path}")

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write("@echo off\n")
        f.write("REM Auto-generated CMD environment snapshot for edge-ai\n")
        f.write(f"REM Captured from: {vsdevcmd}\n\n")
        for k, v in sorted(deltas.items()):
            f.write(f'set "{k}={v}"\n')
    print(f"[+] Exported CMD script: {bat_path}")

    print("\n[+] Environment capture completed successfully.")

if __name__ == "__main__":
    main()
