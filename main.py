#!/usr/bin/env python3
"""The One-Liner Groan-Off — make.fun entry.

Writes a single original one-line dad joke to /output/entry.txt.

The joke: "I tried to make the bed laugh — it said it was already in stitches."
A double pun: "in stitches" means both laughing uncontrollably and the
literal stitching of bedding, so the punchline lands on the very last word
with no wasted setup. 67 characters, one line, UTF-8.

Usage:
    python3 main.py [--output PATH] [--self-test]

--self-test validates the gate: the entry file is UTF-8 text of 1 to 140
characters, not only whitespace, a single line with no leading or trailing
whitespace.
"""

import argparse
import sys
from pathlib import Path

JOKE = "I tried to make the bed laugh \u2014 it said it was already in stitches."

DEFAULT_OUTPUT = Path("/output/entry.txt")


def build_entry() -> str:
    """Return the entry text exactly as it must be written."""
    return JOKE


def write_entry(output: Path) -> Path:
    """Write the entry text to *output* (no trailing newline)."""
    text = build_entry()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return output


def self_test(output: Path | None = None) -> bool:
    """Validate the gate against the entry text (or an existing file)."""
    if output is not None and output.exists():
        raw = output.read_bytes()
        text = raw.decode("utf-8")  # raises on invalid UTF-8
    else:
        text = build_entry()
        raw = text.encode("utf-8")

    problems: list[str] = []
    if not 1 <= len(text) <= 140:
        problems.append(f"length {len(text)} chars, must be 1-140")
    if not text.strip():
        problems.append("entry is only whitespace")
    if text != text.strip():
        problems.append("leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if raw != text.encode("utf-8"):
        problems.append("round-trip UTF-8 mismatch")

    print(f"chars: {len(text)}  bytes: {len(raw)}")
    print(f"entry: {text!r}")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return False
    print("self-test: PASS")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="where to write entry.txt (default: /output/entry.txt)")
    parser.add_argument("--self-test", action="store_true",
                        help="validate the gate instead of writing")
    args = parser.parse_args(argv)

    if args.self_test:
        return 0 if self_test() else 1

    path = write_entry(args.output)
    # Verify what actually landed on disk, not just what we meant to write:
    # re-read the file and run the full gate validation against its bytes.
    if not self_test(path):
        print("FAIL: written file did not pass the gate", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(JOKE)} chars, {len(JOKE.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
