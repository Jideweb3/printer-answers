"""The Printer Finally Answers — entry program.

Writes one line, the office printer's comeback, to entry.txt in the
output directory named by MAKEFUN_OUTPUT_DIR (default /output).

Standard library only. Deterministic: the same line every run.
"""

import os

LINE = "I jammed on page 47 of your 48-page report, and yes, I chose page 47."


def validate(text):
    """The gate, enforced in-program: 1-240 chars, single line, no
    leading/trailing whitespace, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= 240):
        raise ValueError("entry must be 1-240 characters, got %d" % len(text))
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    validate(LINE)

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
        f.write("\n")
    os.chmod(path, 0o644)

    # Read back and verify byte-exactly what actually landed on disk.
    # The file must be precisely LINE + "\n" in UTF-8, checked on raw
    # bytes — no stripping, so a stray trailing space, an extra newline,
    # or a wrong encoding is caught instead of being hidden.
    expected = (LINE + "\n").encode("utf-8")
    with open(path, "rb") as f:
        written = f.read()
    if written != expected:
        raise ValueError(
            "read-back is not byte-exact: expected %d bytes, got %d"
            % (len(expected), len(written))
        )
    validate(written.decode("utf-8").rstrip("\n"))

    print("wrote %s (%d chars)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
