#!/usr/bin/env python3
"""
inspect_src.py
Inspects files in src/ to check headers, docstrings, and documentation links.
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = ROOT_DIR / "src"

def inspect_src():
    print("==================================================")
    print("          SRC DIRECTORY & DOC LINK INSPECTOR      ")
    print("==================================================")
    
    if not SRC_DIR.exists():
        print("   [!] src/ directory not found.")
        return

    file_count = 0
    for path in sorted(SRC_DIR.rglob("*")):
        if path.is_file():
            if "target" in path.parts:
                continue
            file_count += 1
            rel_path = path.relative_to(ROOT_DIR)
            print(f"\n[File {file_count}] {rel_path}")
            
            # Read first 15 lines to check for comments/docstrings/links
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = [f.readline() for _ in range(15)]
                
                doc_found = False
                for line in lines:
                    stripped = line.strip()
                    if any(keyword in stripped.lower() for keyword in ["doc", "spec", "http", "ref", "note", "author", "brief", "///", "//!"]):
                        print(f"   > {stripped}")
                        doc_found = True
                if not doc_found:
                    print("   (No explicit doc link or reference found in header comments)")
            except Exception as e:
                print(f"   [Error reading file: {e}]")
    print("==================================================")

if __name__ == "__main__":
    inspect_src()
