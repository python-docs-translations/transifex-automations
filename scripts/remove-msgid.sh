#!/bin/bash
# Patch POT to solve issues with source messages

set -euo pipefail
IFS=$'\n\t'

# Check if a valid POT directory was passed in command-line interface.
# If no argument is passed, use current working directory .
if [ $# -lt 1 ]; then
    if [[ "$(basename $PWD)" != "pot" ]]; then
        echo "Error: Not in 'pot' directory and no path to pot directory passed."
        exit 1
    fi
else
    if [ $# -gt 1 ]; then
        echo "Ignoring extra arguments, sticking with '$1' ..."
    fi
    if [[ ! -d $1 || "$(basename $1)" != "pot" ]]; then
        echo "'$1' is not a valid directory. Expected a directory named 'pot'."
    fi

    # Enter the given directory
    cd $1
fi

# Create temporary files and set up exit trap
tmp=$(mktemp --suffix='.po')
tmp2=$(mktemp --suffix='.po')
trap 'rm -f $tmp $tmp2' EXIT


# Usage: remove_msgid </path/to/pot> <source message text>
remove_msgid() {
    pot=$1
    shift
    msgid=$@
    if [ ! -f $pot ]; then
        echo "$pot was not found, skipping"
    else
        msggrep -Ke "$msgid" $pot > $tmp
        msgcomm --no-wrap --less-than=2 $pot $tmp > $tmp2
        mv $tmp2 $pot
        echo "Stripping from '$pot': $msgid"
        powrap -q $pot
    fi
}


# \\N is treated as new line in Transifex, so it is an illegal source string
# https://github.com/python-docs-translations/transifex-automations/issues/15
remove_msgid  library/codecs.pot '^\\N$'
remove_msgid  library/re.pot  '^\\N$'
remove_msgid  reference/lexical_analysis.pot  '^\\N$'

# "object" is too common, and should not be translated in this case.
# Remove to avoid incorrect translation.
remove_msgid library/string.templatelib.pot '^object$'
