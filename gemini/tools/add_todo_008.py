#!/usr/bin/env python3
"""
add_todo_008.py
Appends TODO-008 for GitHub billing endpoint migration and scope requirements.
"""
from pathlib import Path

def main():
    print("[+] Starting execution: add_todo_008.py")
    root_dir = Path(__file__).resolve().parent.parent.parent
    backlog_path = root_dir / "gemini" / "backlog.yaml"
    
    entry = """  - id: "TODO-008"
    title: "Adapt GitHub billing audit script to new endpoints (HTTP 410) and admin:org scope"
    status: "backlog"
    priority: "medium"
    documentation_ref: "gemini/docs/tools_inventory.md"
"""
    with open(backlog_path, "a") as f:
        f.write(entry)
        
    print("[+] Added TODO-008 to backlog.yaml")
    print("[+] Completed execution: add_todo_008.py")

if __name__ == "__main__":
    main()
