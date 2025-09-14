#!/bin/bash
# Remove PO files with 0% translation. Takes a root directory as argument.
# e.g.:
#   remove_untranslated.sh cpython/Doc/locales

set -e

trap "rm -vf $po" 1 2 3 6

if [ -n "$1" ]; then
  cd "$1"
fi

pofiles=$(find * -name '*.po' | sort)
to_remove=()
for po in $pofiles; do
  output=$(LC_ALL=C /usr/bin/msgfmt -cvo /dev/null $po 2>&1 | grep -E '[0-9] translated message')
  if $(echo $output | grep '^0 translated messages' > /dev/null); then
    echo "Including to removal: $po"
    to_remove+=($po)
  fi
done

# Check array size. If not 0, then go ahead and remove them
if [ ${#to_remove[@]} -eq 0 ]; then
  echo "No empty PO to remove."
else
  echo -n "Removing... "
  if rm ${to_remove[@]}; then
    echo "Done!"
  else
    echo "Failed!"
  fi
fi
