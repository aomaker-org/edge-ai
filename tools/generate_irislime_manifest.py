#!/usr/bin/env python3
"""
tools/generate_irislime_manifest.py

Scans /home/fekerr/src/irislime and generates:
- edge-ai/irislime/irislime_manifest.json
- edge-ai/irislime/irislime_manifest.md
"""

import os
import json
from pathlib import Path
from datetime import datetime

IRISLIME_ROOT = Path("/home/fekerr/src/irislime")
OUTPUT_DIR = Path("/home/fekerr/src/edge-ai/irislime")

PRUNE_DIRS = {".git", ".venv", "build", ".pytest_cache", "llama.cpp", "deps"}

def classify_file(rel_path: str) -> str:
    path_lower = rel_path.lower()
    
    # 1. Built files
    if (path_lower.startswith(".venv/") or 
        path_lower.startswith("build/") or 
        path_lower.startswith(".pytest_cache/") or 
        path_lower.startswith(".local/") or 
        "__pycache__" in path_lower or 
        path_lower.endswith(".o") or 
        path_lower.endswith(".so") or 
        path_lower.endswith(".a") or 
        rel_path == "uv.lock"):
        return "built_files"

    # 2. Log files & Telemetry Artifacts
    if (path_lower.startswith("logs/") or 
        path_lower.endswith(".log") or 
        path_lower.endswith(".zip") or 
        path_lower.endswith(".csv") or 
        "heartbeat" in path_lower or 
        "telemetry" in path_lower or 
        path_lower.startswith("scratch/") or 
        "scratch_" in path_lower):
        return "log_files"

    # 3. Source files & Documentation
    return "source_files"

def main():
    if not IRISLIME_ROOT.exists():
        print(f"Error: {IRISLIME_ROOT} does not exist.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    manifest_data = {
        "metadata": {
            "source_repo": str(IRISLIME_ROOT),
            "generated_at": datetime.now().isoformat(),
            "timestamp_id": datetime.now().strftime("%y%m%d_%H%M_001"),
            "format_version": "1.0.0"
        },
        "summary": {
            "total_files": 0,
            "total_bytes": 0,
            "counts": {"source_files": 0, "built_files": 0, "log_files": 0},
            "bytes": {"source_files": 0, "built_files": 0, "log_files": 0}
        },
        "files": []
    }

    for root, dirs, files in os.walk(IRISLIME_ROOT):
        # Prune heavy subtrees to avoid traversal overhead while recording top-level references
        for p in list(dirs):
            if p in PRUNE_DIRS or p.startswith("__pycache__"):
                # Track pruned directory as an item
                rel_dir = str((Path(root) / p).relative_to(IRISLIME_ROOT))
                category = "built_files" if p in (".venv", "build", ".pytest_cache") else "source_files"
                manifest_data["files"].append({
                    "path": f"{rel_dir}/",
                    "category": category,
                    "size_bytes": 0,
                    "modified_at": datetime.now().isoformat(),
                    "note": f"Directory pruned for manifest indexing ({p})"
                })
                manifest_data["summary"]["counts"][category] += 1
                dirs.remove(p)

        for f in files:
            full_path = Path(root) / f
            try:
                rel_path = str(full_path.relative_to(IRISLIME_ROOT))
                stat = full_path.stat()
                size = stat.st_size
                category = classify_file(rel_path)

                manifest_data["files"].append({
                    "path": rel_path,
                    "category": category,
                    "size_bytes": size,
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

                manifest_data["summary"]["total_files"] += 1
                manifest_data["summary"]["total_bytes"] += size
                manifest_data["summary"]["counts"][category] += 1
                manifest_data["summary"]["bytes"][category] += size
            except Exception as e:
                print(f"Error processing {full_path}: {e}")

    # Save JSON manifest
    json_path = OUTPUT_DIR / "irislime_manifest.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(manifest_data, jf, indent=2)

    # Save Markdown manifest summary
    md_path = OUTPUT_DIR / "irislime_manifest.md"
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(f"# IrisLime Workspace Full File Manifest\n\n")
        mf.write(f"**Source Repository:** `{IRISLIME_ROOT}`  \n")
        mf.write(f"**Generated:** `{manifest_data['metadata']['generated_at']}`  \n")
        mf.write(f"**Timestamp ID:** `{manifest_data['metadata']['timestamp_id']}`  \n")
        mf.write(f"**Structured Manifest:** [`irislime_manifest.json`](file://{json_path})\n\n")
        mf.write("---\n\n")

        mf.write("## 📊 Summary Breakdown\n\n")
        mf.write("| Classification Category | File Count | Total Size | Description |\n")
        mf.write("| :--- | :--- | :--- | :--- |\n")
        
        c = manifest_data["summary"]["counts"]
        b = manifest_data["summary"]["bytes"]
        
        mf.write(f"| 📄 **Source Files** | {c['source_files']} | {b['source_files'] / (1024*1024):.2f} MB | C/C++ sources, Python modules, Makefiles, docs, configs |\n")
        mf.write(f"| ⚙️ **Built Files** | {c['built_files']} | {b['built_files'] / (1024*1024):.2f} MB | Compiled targets, virtualenv dependencies (`.venv`), build caches |\n")
        mf.write(f"| 📜 **Log Files & Telemetry** | {c['log_files']} | {b['log_files'] / (1024*1024):.2f} MB | Build journals, execution trace logs, diagnostic archives |\n")
        mf.write(f"| **TOTAL** | **{manifest_data['summary']['total_files']}** | **{manifest_data['summary']['total_bytes'] / (1024*1024):.2f} MB** | Full workspace footprint |\n\n")

        mf.write("---\n\n")
        mf.write("## 📂 Category File Samples\n\n")

        for cat, label in [("source_files", "Source Files & Configs"), ("log_files", "Log Files & Telemetry Artifacts"), ("built_files", "Built & Ephemeral Assets")]:
            mf.write(f"### {label}\n\n")
            cat_files = [f for f in manifest_data["files"] if f["category"] == cat]
            mf.write("| File Path | Size (Bytes) | Last Modified |\n")
            mf.write("| :--- | :--- | :--- |\n")
            for item in cat_files[:15]:  # Top 15 samples
                mf.write(f"| `{item['path']}` | {item['size_bytes']:,} | `{item['modified_at']}` |\n")
            if len(cat_files) > 15:
                mf.write(f"| *... and {len(cat_files) - 15} more files* | | |\n")
            mf.write("\n")

    print(f"Manifest generated successfully at {json_path} and {md_path}")

if __name__ == "__main__":
    main()
