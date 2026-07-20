#!/usr/bin/env python3
"""
ai-log-diff/tools/semantic_log_differ.py

Semantic log comparison and anomaly surface detection tool.
Normalizes volatile log noise (timestamps, addresses, thread IDs)
and computes template-based structural deltas between log files.
"""

import re
import json
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# Regex Patterns for Volatile Noise Normalization
NORMALIZATION_PATTERNS = [
    (re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?\b"), "<TIMESTAMP>"),
    (re.compile(r"\b\d{2}:\d{2}:\d{2}(?:\.\d+)?\b"), "<TIME>"),
    (re.compile(r"\b0x[0-9a-fA-F]+\b"), "<HEX_ADDR>"),
    (re.compile(r"\b[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}\b"), "<UUID>"),
    (re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b"), "<NET_ADDR>"),
    (re.compile(r"\b(?:pid|thread|tid|job)[=\s:]*\d+\b", re.IGNORECASE), "<ID>"),
    (re.compile(r"\/tmp\/[a-zA-Z0-9_\-]+"), "<TMP_PATH>")
]

def normalize_line(line: str) -> str:
    cleaned = line.strip()
    for pattern, replacement in NORMALIZATION_PATTERNS:
        cleaned = pattern.sub(replacement, cleaned)
    return cleaned

def extract_template(line: str) -> str:
    # Basic template extraction: replace numbers with wildcard <N>
    template = re.sub(r"\b\d+\b", "<N>", line)
    return template

def parse_log_file(filepath: Path):
    lines = []
    normalized_lines = []
    templates = []
    
    if not filepath.exists():
        return lines, normalized_lines, templates

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f):
            raw = line.rstrip("\n")
            norm = normalize_line(raw)
            tmpl = extract_template(norm)
            lines.append(raw)
            normalized_lines.append(norm)
            templates.append(tmpl)

    return lines, normalized_lines, templates

def compare_logs(file_a: Path, file_b: Path):
    lines_a, norm_a, tmpl_a = parse_log_file(file_a)
    lines_b, norm_b, tmpl_b = parse_log_file(file_b)

    count_a = Counter(tmpl_a)
    count_b = Counter(tmpl_b)

    all_templates = set(count_a.keys()).union(set(count_b.keys()))

    added = []
    removed = []
    frequency_changed = []

    for tmpl in sorted(all_templates):
        ca = count_a.get(tmpl, 0)
        cb = count_b.get(tmpl, 0)
        if ca == 0 and cb > 0:
            added.append({"template": tmpl, "count_in_b": cb})
        elif ca > 0 and cb == 0:
            removed.append({"template": tmpl, "count_in_a": ca})
        elif ca != cb:
            frequency_changed.append({"template": tmpl, "count_in_a": ca, "count_in_b": cb, "delta": cb - ca})

    # Detect errors/warnings in added lines
    error_patterns = re.compile(r"\b(?:error|fail|failed|fatal|exception|crash)\b", re.IGNORECASE)
    added_errors = [item for item in added if error_patterns.search(item["template"])]

    return {
        "metadata": {
            "log_a": str(file_a),
            "log_b": str(file_b),
            "lines_in_a": len(lines_a),
            "lines_in_b": len(lines_b),
            "generated_at": datetime.now().isoformat()
        },
        "summary": {
            "total_unique_templates": len(all_templates),
            "added_templates_count": len(added),
            "removed_templates_count": len(removed),
            "frequency_changed_count": len(frequency_changed),
            "added_errors_count": len(added_errors)
        },
        "added_events": added,
        "removed_events": removed,
        "frequency_changed_events": frequency_changed,
        "added_errors": added_errors
    }

def format_markdown_report(result: dict) -> str:
    meta = result["metadata"]
    summary = result["summary"]
    
    md = []
    md.append(f"# AI Semantic Log Diff Report")
    md.append(f"")
    md.append(f"**Baseline Log A:** `{meta['log_a']}` ({meta['lines_in_a']} lines)  ")
    md.append(f"**Target Log B:** `{meta['log_b']}` ({meta['lines_in_b']} lines)  ")
    md.append(f"**Generated:** `{meta['generated_at']}`  ")
    md.append(f"")
    md.append(f"---")
    md.append(f"")
    md.append(f"## 📊 Diff Summary")
    md.append(f"")
    md.append(f"| Metric | Count | Description |")
    md.append(f"| :--- | :--- | :--- |")
    md.append(f"| 🚨 **New Error Events** | `{summary['added_errors_count']}` | Unexpected error/failure templates in Log B |")
    md.append(f"| ➕ **New Structural Events** | `{summary['added_templates_count']}` | Templates appearing in Log B but not A |")
    md.append(f"| ➖ **Missing Events** | `{summary['removed_templates_count']}` | Templates present in Log A but omitted in B |")
    md.append(f"| 🔄 **Frequency Shift Events** | `{summary['frequency_changed_count']}` | Events with count discrepancies |")
    md.append(f"")
    md.append(f"---")
    md.append(f"")

    if result["added_errors"]:
        md.append(f"## 🚨 New Error Cascades (Target Log B)")
        md.append(f"")
        for err in result["added_errors"]:
            md.append(f"- `[x{err['count_in_b']}]` `{err['template']}`")
        md.append(f"")

    if result["added_events"]:
        md.append(f"## ➕ Added Events (Target Log B)")
        md.append(f"")
        for evt in result["added_events"][:10]:
            md.append(f"- `[x{evt['count_in_b']}]` `{evt['template']}`")
        if len(result["added_events"]) > 10:
            md.append(f"- *... and {len(result['added_events']) - 10} more added events*")
        md.append(f"")

    if result["removed_events"]:
        md.append(f"## ➖ Missing Events (Omitted in Target Log B)")
        md.append(f"")
        for evt in result["removed_events"][:10]:
            md.append(f"- `[was x{evt['count_in_a']}]` `{evt['template']}`")
        if len(result["removed_events"]) > 10:
            md.append(f"- *... and {len(result['removed_events']) - 10} more omitted events*")
        md.append(f"")

    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="AI Semantic Log Differ")
    parser.add_argument("--log-a", type=Path, required=True, help="Baseline log file path")
    parser.add_argument("--log-b", type=Path, required=True, help="Target log file path")
    parser.add_argument("--json-out", type=Path, default=None, help="Output JSON path")
    parser.add_argument("--md-out", type=Path, default=None, help="Output Markdown report path")
    args = parser.parse_args()

    res = compare_logs(args.log_a, args.log_b)

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.json_out, "w", encoding="utf-8") as jf:
            json.dump(res, jf, indent=2)
        print(f"[semantic_log_differ] Saved JSON diff to {args.json_out}")

    md_report = format_markdown_report(res)
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        with open(args.md_out, "w", encoding="utf-8") as mf:
            mf.write(md_report)
        print(f"[semantic_log_differ] Saved Markdown report to {args.md_out}")

    if not args.json_out and not args.md_out:
        print(md_report)

if __name__ == "__main__":
    main()
