#!/usr/bin/env python3
"""
clean_target_artifacts.py
Removes compiled target/ directories from git tracking and ensures they are ignored.
"""

import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def run_cmd(args):
    print(f"Running: {' '.join(args)}")
    subprocess.run(args, cwd=ROOT_DIR, check=True)

def main():
    print("[*] Ensuring target/ is removed from git index...")
    run_cmd(["git", "rm", "-r", "--cached", "src/tools/gix_manifest/target"], )

    print("[*] Adding target/ to root and local .gitignore if not present...")
    gitignore_path = ROOT_DIR / ".gitignore"
    content = ""
    if gitignore_path.exists():
        content = gitignore_path.read_text()
    
    if "target/" not in content:
        with open(gitignore_path, "a") as f:
            f.write("\n# Rust compilation targets\ntarget/\n**/target/\n")
        print("[+] Added target/ exclusions to .gitignore")

    print("[*] Committing cleanup...")
    run_cmd(["git", "add", ".gitignore"])
    run_cmd(["git", "commit", "-m", "chore(git): exclude cargo target artifacts from tracking"])

    print("[*] Pushing updated branch...")
    run_cmd(["git", "push", "origin", "feat/tools-and-src-inventory"])
    print("[+] Branch cleaned and updated successfully!")

if __name__ == "__main__":
    main()
