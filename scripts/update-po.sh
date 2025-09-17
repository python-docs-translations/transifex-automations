#!/bin/bash

set -e


usage() {
  cat <<EOM
usage: $0 [-P|-h] <branch> <locales_dir>

Update existing PO files in <locales_dir> based
on the current state of Python documentation
version <branch>.

<locales_dir> is expected to have language directories
in the structure <lang>/LC_MESSAGES/subdirs_and_files.po

Options:
  -t    Skip POT files regenaration. This assumes locales_dir
        is already have updated POT files and will go ahead
        updating the PO files.
  -p    Skip PO files update with POT file. Useful when you
        what the POT files but without changing PO files.

Example:
  $(basename $0) 3.14 .
  $(basename $0) 3.14 ../transifex-automations
  $(basename $0) -t 3.14 ../transifex-automations
  $(basename $0) -p 3.14 ../transifex-automations
EOM
}


SKIP_POT_UPDATE=0
SKIP_TRANSLATIONS_UPDATE=0
while getopts "tph" o; do
    case "${o}" in
        t)
            SKIP_POT_UPDATE=1
            ;;
        p)
            SKIP_TRANSLATIONS_UPDATE=1
            ;;
        h)
            usage
            exit 0
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))


branch=$1
locales_dir=$2

if [ -z "$branch" ] || [ -z "$locales_dir" ]; then
    echo "Error: Both branch and locales_dir are required"
    usage
    exit 1
fi

locales_dir=$(realpath $locales_dir)

echo "Using branch: $branch"
echo "Using locale directory: $locales_dir"
cd "$locales_dir"

if [ $SKIP_POT_UPDATE -eq 0 ]; then
    cpython_dir=../cpython
    rm -rf $cpython_dir
    git clone --depth 1 --branch "$branch" https://github.com/python/cpython "$cpython_dir"

    echo "Generating pot files"
    cd "$cpython_dir/Doc"
    ln -sr "$locales_dir" locales
    make clean venv
    opts='-E -b gettext -D gettext_compact=0 -d build/doctrees-gettext . build/gettext'
    make build ALLSPHINXOPTS="$opts"

    echo "Moving pot files into locales directory"
    rm -rf locales/pot/*
    (cd build/gettext; cp -a ./* ../../locales/pot/)

    cd locales
fi

if [ $SKIP_TRANSLATIONS_UPDATE -eq 0 ]; then
    langs=$(ls -1 | grep -Ev '(pot|venv|.tx)')
    pot_files=$(find pot/ -name '*.pot' | sort)

    echo "Updating existing PO files using the new POT files"

    for pot in $pot_files; do
        po=$(echo "$pot" | sed 's|^pot/||;s|\.pot|.po|')
        for lang in $langs; do
            if [ -f "$lang/LC_MESSAGES/$po" ]; then
                msgmerge -U -N --backup=off "$lang/LC_MESSAGES/$po" "$pot"
            fi
        done
    done
    powrap $(find . -name '*.po' | sort)
fi
