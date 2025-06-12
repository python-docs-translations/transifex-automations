==============================================
Commands for maintaining a language repository
==============================================

This document contains instructions to guide you on managing your language
repository, hence helping you translate Python's documentation to your language.

See the :doc:`workflows` for an automated alternative to this guide.

These commands are written in Linux Shell, and should work in Windows Subsystem
Linux (WSL), but feel free to use the same logic in other languages e.g. Python.

.. note::
   Where you see ``${LANGCODE}`` in the commands below, replace it with your
   language code (e.g. 'uk', 'pt_BR') or set the variable
   (e.g. ``LANGCODE=pt_BR``) before running the commands.


Clone CPython repository
------------------------

It is necessary to have a local clone of `CPython's source code repository <https://github.com/python/cpython>`_
in order to update translation files and to build translated documentation.

From inside your language repository, run:

.. code-block:: shell

   BRANCH=3.14
   git clone --depth 1 https://github.com/python/cpython --branch $BRANCH

Use ``--depth 1`` to shallow clone, which avoids downloading all the 800 MB of data
from CPython's repository.

Optionally, you could also add ``--no-single-branch`` to ``git clone`` command which
would make all branches available, allowing to switch between one branch and
another. But this is not needed if you are working on the translation of a single branch.


Install requirements
--------------------

Creating a virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Optionally, create a `virtual environment <https://docs.python.org/3/library/venv.html>`_
(short: *venv*) to keep all Python package installations in it, then activate
this venv to ensure commands are run from it:

.. code-block:: shell

   python -m venv .venv
   source .venv/bin/activate

Install Python packages
^^^^^^^^^^^^^^^^^^^^^^^

Update pip and then install the required packages:

.. code-block:: shell

   python -m pip install --upgrade pip
   python -m pip install sphinx-intl>=2.1.0 pomerge powrap sphinx-lint

Alternatively, put all Python packages inside a requirements.txt file and install
it using pip's ``-r`` flag.

Transifex CLI tool
^^^^^^^^^^^^^^^^^^

Install the Transifex CLI client, required to interact with Transifex:

.. code-block:: shell

   cd .venv/bin
   curl -s -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh
   cd ../..

.. note::
   The above commands result in the ``tx`` binary being downloaded into the ``.venv/bin`` directory.
   Feel free to install this tool wherever you want, but preferably in a
   directory already in the PATH so that ``tx`` works without its full path.

Updating the translations
-------------------------

For language teams that coordinate translation efforts on Transifex, updating
translation means pulling the translation strings.

.. admonition:: Recommendation
   Before pulling translations, consider updating the .tx/config to
   have an up-to-date mapping of project/resources. For this, it is required to
   generate the documentation's pot files (template of po files), so start
   with the pot. Alternatively, you can skip it and pull translations, but new
   translation resources in Transifex could be not mapped, and hence wouldn't be pulled.

.. _generate-pot:

Generating pot files
^^^^^^^^^^^^^^^^^^^^

Sphinx's gettext builder can be used for generating pot files:

.. code-block:: shell

   make -C cpython/Doc/ ALLSPHINXOPTS='-E -b gettext -D gettext_compact=0 -d build/.doctrees . locales/pot' build

There should now be a ``cpython/Doc/locales/pot/`` directory containing all of the
pot files.

Generating a .tx/config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have the pot files, make use of sphinx-intl to generate the .tx/config:

.. code-block:: shell

   cd cpython/Doc/locales
   sphinx-intl create-txconfig
   sphinx-intl update-txconfig-resources \
       --transifex-organization-name python-doc \
       --transifex-project-name=python-newest \
       --locale-dir . --pot-dir pot

This step should take some time to finish. Once it is complete, there should be
a ``cpython/Doc/locales/.tx/config`` file containing a list of resources based
on the previously :ref:`generated pot files <generate-pot>`.

As a final touch, we copy the ``.tx/config`` to the language repository making
proper tweaks so one can download translations from Transifex or upload local
translation changes, all this from repository's root directory:

.. code-block:: shell

   cd ../../..   # back to language repository root directory
   mkdir -p .tx
   sed cpython/Doc/locales/.tx/config \
       -e "s|^file_filter  = .*|&\nx&|;" \
       -e "s|^source_file  = pot/|source_file  = cpython/Doc/locales/pot/|" \
       > .tx/config
   sed -i .tx/config \
       -e "s|^xfile_filter  = ./<lang>/LC_MESSAGES/|trans.${LANGCODE}  = |;"

Remapping translation and Transifex resources is complete.

Pulling translations
^^^^^^^^^^^^^^^^^^^^

To download translations from Transifex using Transifex CLI tool:

.. code-block:: shell

   tx pull -l ${LANGCODE} -t -f

Argument explanations:

* ``-l ${LANGCODE}`` – specify the language code so that tx doesn't pull all languages.
* ``-t`` – specify that we want translations
* ``-f`` – force pulling all files, because without this sometimes changes in Transifex are not downloaded

Wrapping the translation files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After pulling, it is highly recommended to use `powrap <https://pypi.org/project/powrap/>`_
on the po files to make them look better:

.. code-block:: shell

   powrap --quiet *.po **/*.po

Alternatively, you can use ``--modified`` flag to save time and apply only to
changed files.


Commit and push translation changes
-----------------------------------

The following commands are recommended for committing and pushing your
translations to your language repository.

.. code-block:: shell

   git diff -I'^"POT-Creation-Date: ' --numstat *.po **/*.po | cut -f3 | xargs -r git add
   git add $(git ls-files -o --exclude-standard *.po **/*.po) .tx/config
   git diff-index --quiet HEAD || { git commit -m "Update translations" && git push; }

It is not recommended to simply ``git add`` (stage) all PO files because this would
also stage (and then commit) the translation files that have only irrelevant
changes in their ``POT-Creation-Date`` header field (i.e. date when the PO was
updated against the POT).

The first command first git-add modified tracked files that does **not**
exclusively match changes in POT-Creation-Date header, hence relevant changes
are included.

The second command will git-add untracked po files that may have been newly
created on the latest 'tx pull' run. It also adds .tx/config file.

The last command will only commit and push if any file was git-added in the
above commands.


Build translated documentation
------------------------------

Useful for testing the translations, spotting syntax errors and viewing the
result of your contribution.

To build translated documentation, run:

.. code-block:: shell

   cp --parents *.po **/*.po cpython/Doc/locales/${LANGCODE}/LC_MESSAGES/
   make -C cpython/Doc venv
   make -C cpython/Doc SPHINXOPTS="--keep-going -D gettext_compact=0 -D language=${LANGCODE}" html

The first command copies the translation files (.po) into cpython's locale_dir,
which is required for it to be recognized.

The second command creates a pre-configured virtual environment using the
Makefile from CPython's Doc directory.

Finally, build using the Makefile. Here is an explanation of the arguments used:

* ``-C cpython/Doc`` – changes the current directory to run the make command
* ``SPHINXOPTS`` – this variable should contain any CLI modifier command you want to pass
* ``--keep-going`` – even if it fails, go all way to the end to bring up all errors
* ``-D gettext_compact=0`` – override sphinx settings to consider one PO file == one doc page
* ``-D language=$LANGCODE`` – override sphinx settings to build in the desired ``$LANGCODE``
* ``html`` – the Makefile target that triggers the Sphinx's html builder


Viewing the documentation in a web browser
------------------------------------------

Just build translated documentation and then open in a browser, no secrets.
See below a one-line command to use your default web browser to open the index.html:

.. code-block:: shell

    python -c "import os, webbrowser; webbrowser.open('file://cpython/Doc/build/html/index.html')"

Notice ``index.html`` can be replaced with any file, e.g. ``'library/os.html'``.


Linting the translation files
-----------------------------

``sphinx-lint`` is great to spot translation errors that will didn't spot e.g.
trailing whitespace in the string, reST directive not properly surrounded with
whitespace, etc. It's highly recommended.

.. code-block:: shell

   sphinx-lint *.po **/*.po


Merging translations into another branch
----------------------------------------

This is useful when you want to replicate a translation from the CPython branch
currently being translated to another older branch. E.g. |py_new| is currently being
translated, but |py_last| has that same string and could make use of the contributed
translations.

.. code-block:: shell

   CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
   TARGET_BRANCH=3.12
   pomerge --from-files *.po **/*.po
   git checkout ${TARGET_BRANCH}
   pomerge --to-files *.po **/*.po

After the above command, the translation from the current branch were applied to
the previous branch |py_last|. Now, one can verify lines are wrapped:

.. code-block:: shell

   powrap --modified *.po **/*.po

Done changing, let's commit and push these changes, and go back the original branch:

.. code-block:: shell

   git diff -I'^"POT-Creation-Date: ' --numstat *.po **/*.po | cut -f3 | xargs -r git add
   git diff-index --quiet HEAD || { git commit -m "Merge translations into ${TARGET_BRANCH}" && git push; }
   git checkout ${CURRENT_BRANCH}
