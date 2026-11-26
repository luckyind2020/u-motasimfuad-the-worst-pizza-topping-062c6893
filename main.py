#!/usr/bin/env python3
"""The Worst Pizza Topping — make.fun entry.

Reads the one-line pitch from entry.txt (kept beside this file),
validates it against the bounty gate (UTF-8 text, a single line of
1 to 200 characters, not only whitespace), writes it to
/output/entry.txt for the grader, and prints it.
"""

from pathlib import Path

MAX_CHARS = 200
ENTRY_FILE = Path(__file__).with_name("entry.txt")
OUTPUT_FILE = Path("/output/entry.txt")


def normalise_line(raw: str) -> str:
    """Drop a UTF-8 BOM and collapse runs of inner whitespace to one space."""
    cleaned = raw.lstrip("\ufeff")
    return " ".join(cleaned.split())


def load_line(path: Path) -> str:
    """Return the single non-empty line from ``path``."""
    text = path.read_text(encoding="utf-8")
    lines = [normalise_line(line) for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        raise ValueError(f"expected exactly one non-empty line, got {len(lines)}")
    return lines[0]


def validate(line: str) -> str:
    """Enforce the bounty gate on the pitch line."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, must be 1-{MAX_CHARS}")
    if line.strip() != line:
        raise ValueError("line must not start or end with whitespace")
    if any(ord(ch) < 0x20 and ch not in "\t" for ch in line):
        raise ValueError("line holds control characters")
    if "pizza" not in line.lower():
        raise ValueError("line must name a pizza")
    return line


def write_output(line: str) -> None:
    """Write the pitch to /output/entry.txt and verify the round-trip."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(line, encoding="utf-8")
    written = OUTPUT_FILE.read_text(encoding="utf-8")
    if written != line:
        raise ValueError("round-trip check failed: output differs from the pitch")
    if not 1 <= len(written) <= MAX_CHARS:
        raise ValueError(f"output is {len(written)} chars, must be 1-{MAX_CHARS}")


def main() -> None:
    line = validate(load_line(ENTRY_FILE))
    write_output(line)
    print(line)


if __name__ == "__main__":
    main()
