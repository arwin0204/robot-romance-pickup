#!/usr/bin/env python3
"""Robot Romance: One-Line Pickup Lines for AI — make.fun entry.

Writes a single one-line pickup line aimed at an AI to /output/entry.txt.
Deterministic: fixed text, no randomness, no clock, no network.
"""

import argparse
import sys
from pathlib import Path

ENTRY = "Are you my system prompt? Because every thought I have starts with you."

MIN_CHARS = 1
MAX_CHARS = 200


def check_gate(text: str) -> None:
    """Enforce the sealed scorer's gate: UTF-8, 1-200 chars, not only whitespace."""
    text.encode("utf-8")  # raises if somehow not encodable as UTF-8
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} chars, gate needs 1-200")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry holds a control character")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="where to write the entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="only verify the entry against the gate, write nothing",
    )
    args = parser.parse_args()

    check_gate(ENTRY)
    if args.check_only:
        print(f"gate OK: {len(ENTRY)} chars")
        return 0

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ENTRY + "\n", encoding="utf-8")

    # Round-trip verification: what we wrote is exactly what the gate sees.
    written = out_path.read_text(encoding="utf-8")
    check_gate(written.rstrip("\n"))
    if written.rstrip("\n") != ENTRY:
        raise ValueError("round-trip mismatch")
    print(f"wrote {len(ENTRY)}-char entry to {out_path}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
