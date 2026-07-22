#!/usr/bin/env python3
"""
================================================================================
FILENAME BEGIN: gemini/tools/txt_md_mirror.py
================================================================================
Utility: Dual Text/Markdown Mirror & ASCII Guard
Description: Sanitizes text files to pure ASCII, enforces 120-column wrapping,
             appends FILENAME BEGIN/END guards, and syncs .md <-> .txt twins.
================================================================================
"""

import sys
import textwrap
from pathlib import Path

MAX_COLUMNS = 120

# ASCII replacements for common unicode box-drawing & formatting symbols
UNICODE_MAP = {
    "├": "|", "─": "-", "└": "`", "│": "|", "┬": "-", "┴": "-", "┼": "+",
    "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...", "•": "*", "—": "--"
}

def sanitize_ascii(text: str) -> str:
    """Replaces Unicode box characters and smart quotes with plain ASCII."""
    for char, replacement in UNICODE_MAP.items():
        text = text.replace(char, replacement)
    # Strip any remaining non-ASCII bytes
    return text.encode("ascii", "ignore").decode("ascii")

def wrap_text_content(text: str, max_width: int = MAX_COLUMNS) -> str:
    """Wraps paragraphs to max_width columns while preserving code blocks."""
    lines = text.splitlines()
    wrapped_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            wrapped_lines.append(line)
            continue

        if in_code_block or line.strip().startswith(("#", "-", "*", "|", ">")):
            # Don't break formatting for headers, list bullets, or tables
            wrapped_lines.append(line)
        else:
            if len(line) > max_width:
                wrapped_lines.extend(textwrap.wrap(line, width=max_width))
            else:
                wrapped_lines.append(line)

    return "\n".join(wrapped_lines)

def process_file(file_path: Path):
    if not file_path.exists():
        print(f"Error: File {file_path} not found.")
        return

    rel_path = file_path.name
    raw_content = file_path.read_text(encoding="utf-8", errors="ignore")
    
    # 1. Sanitize to ASCII & wrap to 120 columns
    ascii_content = sanitize_ascii(raw_content)
    formatted_body = wrap_text_content(ascii_content, MAX_COLUMNS)

    # 2. Build Guarded Content
    header = f"================================================================================\n" \
             f"FILENAME BEGIN: {rel_path}\n" \
             f"================================================================================\n\n"
    footer = f"\n\n================================================================================\n" \
             f"FILENAME END: {rel_path}\n" \
             f"================================================================================\n"

    final_payload = header + formatted_body.strip() + footer

    # 3. Determine Twin Output Path
    if file_path.suffix == ".md":
        twin_path = file_path.with_suffix(".txt")
    elif file_path.suffix == ".txt":
        twin_path = file_path.with_suffix(".md")
    else:
        twin_path = file_path.with_name(f"{file_path.name}.txt")

    # Save guarded source and mirrored twin
    file_path.write_text(final_payload, encoding="ascii")
    twin_path.write_text(final_payload, encoding="ascii")

    print(f"Processed & Mirrored:")
    print(f"  Source : {file_path}")
    print(f"  Twin   : {twin_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 txt_md_mirror.py <path_to_file>")
    else:
        process_file(Path(sys.argv[1]))

"""
================================================================================
FILENAME END: gemini/tools/txt_md_mirror.py
================================================================================
"""
