import polib
import re
from pathlib import Path

# Patterns for the messages that do not need to be translated
regex_patterns = (
    re.compile(r"^\d+$"),  # all digits
)


def process_pot(pot_path):
    pot = polib.pofile(pot_path)
    changed = False

    for entry in pot:
        for pattern in regex_patterns:
            if not entry.translated() and pattern.match(entry.msgid):
                if (
                    "grp" in pot_path.name
                ):  # Trial period, just library/grp.pot which has msgids: "0", "1", "2", "3"
                    entry.msgstr = entry.msgid
                    changed = True
                    print(f"[{pot_path}] Copied '{entry.msgid}'")

    if changed:
        pot.save()


def main():
    for path in Path(".").rglob("*.pot"):
        process_pot(path)


if __name__ == "__main__":
    main()
