#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/build_runner.py
================================================================================
Utility: WSL2 Out-of-Tree Build Runner & Telemetry Extractor
Description: Creates structured build subfolders with immutable logs and 
             JSON metadata sidecars.
================================================================================
"""

import sys
import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def get_git_info():
    """Captures exact commit hash and dirty status for forensic traceability."""
    def _run(cmd):
        try:
            return subprocess.check_output(cmd, shell=True, cwd=REPO_ROOT, text=True).strip()
        except Exception:
            return "unknown"
            
    return {
        "commit": _run("git rev-parse HEAD"),
        "branch": _run("git rev-parse --abbrev-ref HEAD"),
        "is_dirty": len(_run("git status --porcelain")) > 0
    }

def run_build(target="x86_64_host", config="debug", build_cmd="make -j$(nproc)"):
    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    
    # Enforce Out-of-Tree Build Folder Matrix
    build_dir = REPO_ROOT / "build" / "wsl_ubuntu" / target / config
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Enforce Log Archival Directory ("Precious Logs")
    logs_dir = REPO_ROOT / "logs" / "builds" / f"{datetime.now().strftime('%Y-%m')}"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    log_filename = f"{timestamp_str}_{target}_{config}.log"
    log_path = logs_dir / log_filename
    meta_path = logs_dir / f"{timestamp_str}_{target}_{config}_metadata.json"
    
    print(f"==================================================")
    print(f" Starting WSL Build Target : {target} [{config}]")
    print(f" Build Directory           : {build_dir}")
    print(f" Precious Log Destination  : {log_path}")
    print(f"==================================================")
    
    start_time = time.time()
    
    # Execute build and capture stdout + stderr simultaneously
    with open(log_path, "w", encoding="utf-8") as log_file:
        proc = subprocess.Popen(
            build_cmd,
            shell=True,
            cwd=build_dir if (build_dir / "Makefile").exists() or (build_dir / "CMakeCache.txt").exists() else REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Stream live to terminal while piping to log file
        for line in proc.stdout:
            sys.stdout.write(line)
            log_file.write(line)
            
        proc.wait()
        
    duration = round(time.time() - start_time, 2)
    exit_code = proc.returncode
    
    # Generate Forensic Metadata Sidecar for Future ML Parsing
    metadata = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "target_arch": target,
        "configuration": config,
        "build_command": build_cmd,
        "exit_code": exit_code,
        "duration_seconds": duration,
        "git_state": get_git_info(),
        "environment": {
            "user": os.environ.get("USER", "unknown"),
            "host": os.environ.get("HOSTNAME", "wsl2"),
            "python_version": sys.version.split()[0],
        },
        "log_file": str(log_path.relative_to(REPO_ROOT))
    }
    
    meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    
    print(f"\n[Build Complete] Exit Code: {exit_code} | Duration: {duration}s")
    print(f"Metadata written to: {meta_path}")

if __name__ == "__main__":
    target_arg = sys.argv[1] if len(sys.argv) > 1 else "x86_64_host"
    config_arg = sys.argv[2] if len(sys.argv) > 2 else "debug"
    cmd_arg = sys.argv[3] if len(sys.argv) > 3 else "make -j$(nproc)"
    
    run_build(target=target_arg, config=config_arg, build_cmd=cmd_arg)

"""
================================================================================
FILENAME END: gemini/tools/build_runner.py
================================================================================
"""
