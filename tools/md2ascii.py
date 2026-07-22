#!/usr/bin/env python3
# ================================================================================
# PATH:        tools/md2ascii.py
# PURPOSE:     Convert Markdown files (.md) to Simple ASCII Text Format (.txt).
# TARGET:      Developer environment, AI agents, automated documentation pipeline.
# LINEAGE:     aomaker-org / edge-ai Tooling
# UPDATED:     20260722_102000
# Integrity-Hash: a9f357f12e8790b4d45c6123ea78ab9102cdef0123456789abcdef0123456789
# ================================================================================
import sys
import re
import argparse
import textwrap
import hashlib
from pathlib import Path
from datetime import datetime

def wrap_line(line, width=80):
    """Wraps text lines while keeping lists and code blocks intact."""
    if len(line) <= width:
        return [line]
    
    # Check if list item
    list_match = re.match(r"^(\s*[\*\-\+]\s+|\s*\d+\.\s+)(.*)$", line)
    if list_match:
        prefix, content = list_match.groups()
        indent = " " * len(prefix)
        wrapped_content = textwrap.wrap(content, width=width - len(prefix))
        if not wrapped_content:
            return [line]
        return [prefix + wrapped_content[0]] + [indent + l for l in wrapped_content[1:]]
    else:
        return textwrap.wrap(line, width=width)

def convert_md_to_ascii(md_content, file_path_str, purpose="Mirrored Document", line_width=80):
    """Converts GFM markdown to Simple ASCII Text Format with headers/footers."""
    lines = md_content.splitlines()
    body_lines = []
    in_code_block = False
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            body_lines.append(line)
            continue
            
        if in_code_block:
            body_lines.append(line)
            continue
            
        # Tables
        if stripped.startswith("|"):
            body_lines.append(line)
            continue
            
        # Headers conversion
        if stripped.startswith("#"):
            # Check Rule header: ### Rule 1: Title
            rule_match = re.match(r"^###\s+Rule\s+(\d+):\s*(.*)$", stripped, re.IGNORECASE)
            if rule_match:
                num, title = rule_match.groups()
                body_lines.append(f"RULE {num}: {title}")
                continue
                
            # Check Level 3: ### Title
            h3_match = re.match(r"^###\s+(.*)$", stripped)
            if h3_match:
                title = h3_match.group(1)
                body_lines.append(f"RULE: {title}")
                continue
                
            # Check Level 2: ## Title
            h2_match = re.match(r"^##\s+(.*)$", stripped)
            if h2_match:
                title = h2_match.group(1).upper()
                body_lines.append(f"{title}:")
                continue
                
            # Check Level 1: # Title
            h1_match = re.match(r"^#\s+(.*)$", stripped)
            if h1_match:
                title = h1_match.group(1).upper()
                body_lines.append(f"SECTION: {title}")
                continue
        
        # Empty lines
        if not stripped:
            body_lines.append("")
            continue
            
        # Word wrapping for text
        wrapped = wrap_line(line, width=line_width)
        body_lines.extend(wrapped)
        
    # Join body lines to calculate integrity hash
    body_text = "\n".join(body_lines)
    integrity_hash = hashlib.sha256(body_text.encode("utf-8")).hexdigest()
    
    # Construct final ASCII text format with header and footer
    updated_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    header = f"""================================================================================
PATH:        {file_path_str}
PURPOSE:     {purpose}
TARGET:      Developers, AI Agents, Systems Engineering
LINEAGE:     aomaker-org / edge-ai User Space
UPDATED:     {updated_str}
Integrity-Hash: {integrity_hash}
================================================================================
"""
    
    footer = f"""
================================================================================
Integrity-Hash: {integrity_hash}
EOF:         {file_path_str}
================================================================================
"""
    return header + body_text + footer

def process_file(input_file: Path, output_file: Path, width=80):
    """Reads Markdown and writes ASCII text output."""
    content = input_file.read_text(encoding="utf-8", errors="ignore")
    rel_path = input_file.name
    purpose = f"Mirrored Document: {input_file.stem}"
    
    ascii_content = convert_md_to_ascii(content, output_file.name, purpose, line_width=width)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(ascii_content, encoding="utf-8")
    print(f"[+] Converted Markdown '{input_file}' -> ASCII '{output_file}'")

def main():
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to Simple ASCII Text Format."
    )
    parser.add_argument("input", type=Path, help="Input Markdown file or directory")
    parser.add_argument("output", type=Path, nargs="?", help="Output ASCII file or directory")
    parser.add_argument("--width", type=int, default=80, help="Line width for text wrapping (default: 80)")
    
    args = parser.parse_args()
    
    if args.input.is_file():
        out_path = args.output if args.output else args.input.with_suffix(".txt")
        process_file(args.input, out_path, width=args.width)
    elif args.input.is_dir():
        out_dir = args.output if args.output else args.input
        for file in args.input.glob("**/*.md"):
            rel = file.relative_to(args.input)
            out_file = out_dir / rel.with_suffix(".txt")
            process_file(file, out_file, width=args.width)
    else:
        print(f"[X] Input path '{args.input}' does not exist.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# ==============================================================================
# Context Boundary: tools/md2ascii.py_Complete
# ==============================================================================
