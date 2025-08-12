#!/usr/bin/env python3
"""
Check .po files for presence of specific language patterns in translated strings.
Languages currently checked: Russian, Polish, Ukranian.
"""
import argparse
import re
import polib
from pathlib import Path

# Character patterns
RUSSIAN = r"\u0400-\u04FF"  # Full Cyrillic block
POLISH = r"ĄĆĘŁŃŚŹŻąćęłńśźż"
UKRAINIAN = r"ҐЄІЇґєії"


def build_pattern(enable_russian=True, enable_polish=True, enable_ukrainian=True):
    """
    Build a compiled regex pattern for the selected languages.
    """
    parts = []
    if enable_russian:
        parts.append(RUSSIAN)
    if enable_polish:
        parts.append(POLISH)
    if enable_ukrainian:
        parts.append(UKRAINIAN)
    if not parts:
        return None
    return re.compile(f"[{''.join(parts)}]")


def find_matches_in_po(po_path, pattern):
    """
    Search for matches in translated strings of a PO file.
    Skips entries with empty translations.
    """
    matches = []
    if not pattern:
        return matches

    po = polib.pofile(po_path)
    for entry in po:
        # Skip if there is no translation at all
        if not entry.msgstr.strip() and not any(v.strip() for v in entry.msgstr_plural.values()):
            continue

        texts = [entry.msgstr]

        for text in texts:
            if text and pattern.search(text):
                matches.append((po_path, entry.linenum, text))
                break  # avoid multiple reports for the same entry
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="One or more PO files or directories to search")
    parser.add_argument("--no-russian", action="store_true", help="Disable Russian pattern checking.")
    parser.add_argument("--no-polish", action="store_true", help="Disable Polish pattern checking.")
    parser.add_argument("--no-ukrainian", action="store_true", help="Disable Ukrainian pattern checking.")

    args = parser.parse_args()

    pattern = build_pattern(
        enable_russian=not args.no_russian,
        enable_polish=not args.no_polish,
        enable_ukrainian=not args.no_ukrainian
    )

    if not pattern:
        parser.error("All checks are disabled. Enable at least one language pattern.")

    paths = []
    for arg in args.paths:
        p = Path(arg)
        if p.is_dir():
            paths.extend(p.rglob("*.po"))
        elif p.is_file():
            paths.append(p)
        else:
            print(f"Warning: {p} not found.")

    for path in paths:
        for po_path, linenum, text in find_matches_in_po(path, pattern):
            print(f"{po_path}:{linenum}: {text}")


if __name__ == "__main__":
    main()
