#!/usr/bin/env python3
"""
Check PO files for translations from another language
"""
import argparse
import re
from pathlib import Path

import polib
from iso639 import Lang
from pyfranc import franc


# $ ls -1 | grep -Poh '([a-z]{3}|[a-z]{2})' | grep -Ev '(pot|en)' | sort -u | tr '\n' ' '
# TODO: de-hardcode this.
# Languages currently available in transifex-automations, without region
ALLOWED_LANGUAGES = [
    "ans", "ar", "az", "bn", "ca", "cmn", "cs", "da", "de", "el", "es", "fa",
    "fi", "hi", "hu", "id", "it", "ja", "ka", "ko", "ky", "lt", "mr", "nb",
    "ne", "nl", "pl", "ps", "pt", "ru", "si", "sq", "sv", "tr", "uk", "ur",
    "vi", "zh"
]

LANGUAGE_PATTERN = r"([a-z]{3}|[a-z]{2})"


def get_lang_from_file(po: polib.POFile) -> str | None:
    """
    Extract language from metadata['Language'], match the language pattern,
    and return ISO 639-3 equivalent.
    Returns None if language metadata is missing or invalid.
    """
    lang = po.metadata.get('Language', '')
    match = re.match(LANGUAGE_PATTERN, lang)
    try:
        lang_code_2 = match.group(0)
        return Lang(lang_code_2).pt3  # ISO 639-3 code
    except (AttributeError, KeyError):
        return None


def convert_language_list_to_iso639_3(allowed_languages: list) -> list:
    """
    Generate a ISO 639-3 list from the existing language list as downloaded
    from Transifex. Handles lang nameas as "ru", "pt_BR", "cmn" and "es_419"
    """
    converted = sorted([
        Lang(l).pt3 if len(l) == 2 else l
        for l in allowed_languages
    ])
    return converted


def detect_language_from_text(text: str, allowed_languages: list) -> str | None:
    """
    Return the ISO 639-3 language code as detected by pyfranc's franc function,
    or return None if matches nothing, if undefined or not a 100% match.
    """
    found = franc.lang_detect(text, whitelist = allowed_languages)
    if found and not found[0][0] == 'und':
        return found[0][0]  # returns ISO 639-3
    else:
        return None


def find_matches_in_po(po_path: str, delete_matches: bool = False, allowed_languages: list = []):
    """
    Compare expected language from metadata with detected language from msgstr.
    If different, record the entry. Optionally delete mismatched translations.
    """
    matches = []
    po = polib.pofile(po_path)
    expected_lang = get_lang_from_file(po)
    modified = False

    if not expected_lang:
        return matches # skip if no valid expected language

    for entry in po:
        # Skip if there is no translation at all
        if not entry.msgstr.strip():
            continue

        detected_lang = detect_language_from_text(
            entry.msgstr, allowed_languages
        )

        if detected_lang != expected_lang and detected_lang:
            matches.append((po_path, entry.linenum, detected_lang, entry.msgstr))
            if delete_matches:
                entry.msgstr = ""
                modified = True

        if delete_matches and modified:
            po.save()

    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="+", help="One or more PO files or directories to search"
    )
    parser.add_argument(
        "--delete-matches",
        action="store_true",
        help="Delete msgstr of matched entries.",
    )
    parser.add_argument(
        "--lang",
        metavar="LANG",
        help="Specific language (2- or 3-letter code) to compare translations against. "
             "If not set, will check against all allowed languages."
    )

    args = parser.parse_args()

    if args.lang:
        allowed_list = convert_language_list_to_iso639_3([args.lang])
    else:
        allowed_list = convert_language_list_to_iso639_3(ALLOWED_LANGUAGES)

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
        for po_path, linenum, detected_lang, text in find_matches_in_po(
            path, args.delete_matches, allowed_list
        ):
            print(f"{po_path}:{linenum}: [{detected_lang}] {text}")


if __name__ == "__main__":
    main()
