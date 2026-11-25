#!/usr/bin/env python3
"""One-line resignation letter of a forgotten staging cron job.

Stdlib only, no network, deterministic. Writes the single entry line
to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set),
creating the directory first, and echoes the same line to stdout.

The voice is the flat, tired cron job nobody disabled: it has mailed
test@example.com every day for a year, and the silence from the inbox
matches the silence from its owner.
"""

import os
import sys
from pathlib import Path

ENTRY_TEXT = (
    "I resign. I'm the cron job you left running in staging. "
    "I've emailed test@example.com daily for a year. "
    "He never replies. Neither do you."
)

MAX_CHARS = 140


def validate(text: str) -> list[str]:
    """List every gate rule the candidate line breaks (empty is clean)."""
    issues = []
    if not text:
        issues.append("entry is empty")
    if len(text) > MAX_CHARS:
        issues.append(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        issues.append("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        issues.append("entry must be a single line")
    if text and not text.strip():
        issues.append("entry is only whitespace")
    return issues


def target_dir() -> Path:
    """Output directory: $MAKEFUN_OUTPUT_DIR when set, else /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def emit(text: str) -> None:
    """Create the output directory, write entry.txt, echo to stdout."""
    folder = target_dir()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "entry.txt").write_text(text, encoding="utf-8")
    print(text)


def main() -> int:
    """Validate the resignation line, then emit it. Returns exit code."""
    line = ENTRY_TEXT.strip()
    problems = validate(line)
    if problems:
        print("invalid entry: " + "; ".join(problems), file=sys.stderr)
        return 1
    emit(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
