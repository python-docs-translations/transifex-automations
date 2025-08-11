#!/usr/bin/env python3
import argparse
import re
import polib
from pathlib import Path

# Russian letters (Cyrillic Unicode block)
RUSSIAN_PATTERN = r'[\u0400-\u04FF]'

# Specific Polish letters
POLISH_PATTERN = r'[ĄĆĘŁŃÓŚŹŻąćęłńóśźż]'


def build_pattern(check_russian=True, check_polish=True):
    """Build the combined regex based on selected languages."""
    parts = []
    if check_russian:
        parts.append(RUSSIAN_PATTERN)
    if check_polish:
        parts.append(POLISH_PATTERN)
    if not parts:
        return None
    return re.compile("|".join(parts))


def find_matches_in_po(po_path, regex):
    po = polib.pofile(po_path)
    matches = []
    for entry in po:
        texts = [entry.msgid, entry.msgstr]
        if entry.msgid_plural:
            texts.extend(entry.msgid_plural.values())

        for text in texts:
            if text and regex.search(text):
                matches.append((po_path, entry.linenum, text))
                break  # avoid multiple reports for the same entry
    return matches


def main():
    parser = argparse.ArgumentParser(
        description="Search for Russian and/or Polish patterns in PO files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more PO files or directories to search"
    )
    parser.add_argument(
        "--no-russian",
        action="store_true",
        help="Disable Russian text detection"
    )
    parser.add_argument(
        "--no-polish",
        action="store_true",
        help="Disable Polish text detection"
    )
    args = parser.parse_args()

    regex = build_pattern(not args.no_russian, not args.no_polish)
    if regex is None:
        parser.error("All checks are disabled. Enable at least one language.")

    po_files = []
    for arg in args.paths:
        p = Path(arg)
        if p.is_dir():
            po_files.extend(p.rglob("*.po"))
        elif p.is_file():
            po_files.append(p)
        else:
            print(f"Warning: {p} not found.")

    for path in po_files:
        for po_path, linenum, text in find_matches_in_po(path, regex):
            print(f"{po_path}:{linenum}: {text}")


if __name__ == "__main__":
    main()
