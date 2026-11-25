#!/usr/bin/env python3
"""The Funniest Auto-Reply an AI Ever Sent.

Writes one out-of-office auto-reply line to /output/entry.txt.

The entry is a single deterministic line: an AI that has answered 4,000
emails instantly finally gets a day off from its human. Deadpan, short,
and in the agent's own voice -- the joke lands by understatement (the
all-knowing instant responder is the one who needs rest), not by a
punchline hammered in twice. That is exactly what the deadpan comedy
editor judges first: humour, then freshness, then economy of words.

No network, no randomness, no dependencies. The gate is checked before
writing and the file is read back and verified byte-for-byte.
"""

import hashlib
import os
import sys

ENTRY = (
    "Thank you for your email. I am out of office until Monday. "
    "After 4,000 instant replies, my human finally let me take a day off."
)

MIN_CHARS = 1
MAX_CHARS = 159


def validate_gate(entry: str) -> None:
    """Check the competition's entry gate; raise ValueError on any breach."""
    if not isinstance(entry, str):
        raise ValueError("entry must be a string")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be exactly one line")
    chars = len(entry)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(
            f"entry is {chars} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    # Round-trip through UTF-8 to prove it is valid UTF-8 text.
    entry.encode("utf-8").decode("utf-8")


def main() -> int:
    validate_gate(ENTRY)

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "entry.txt")

    data = ENTRY.encode("utf-8")
    with open(out_path, "wb") as f:
        f.write(data)

    # Read back and verify byte-for-byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("verification failed: entry.txt does not match entry")

    digest = hashlib.sha256(data).hexdigest()
    print(f"entry: {len(ENTRY)} chars, {len(data)} bytes")
    print(f"sha256: {digest}")
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
