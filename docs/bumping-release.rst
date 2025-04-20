====================================================
Bumping python-newest to latest Python release
====================================================

NOTE: This doc is out of date and needs rework! The `pull request \#13 <https://github.com/python-docs-translations/transifex-automations/pull/13>`_ is a work in progress that would change some instructions from this guide.

This document aims to list the steps required for updating version of the 'Python' project (slug 'python-newest) in python-doc organization in Transifex.

1. Back up current translations:

    #. Run ``sh scripts/update.sh`` to set up the environment, if not done already;
    #. Run ``python3 scripts/getlangs.py`` to get a list of all languages;
    #. Change to ``cpython/Doc/locales`` directory; and
    #. Run ``tx pull --languages <LANGUAGES>`` to download translations from Transifex, replacing ``<LANGUAGES>`` with the output of step 1.2.

2. Post a Python version upgrade announcement

3. (How?) Lock all resources in python-newest for all languages

     #. Take note of the last change in timeline and its timestamp: *Python* > *Settings* > *Timeline*.

4. Create a Transifex project with versioned name to receive python-newest's translations, setting it with the following values:

:*Name your project*: Python <version> (e.g. Python 3.10)
:*URL to opensource license*: https://github.com/python/cpython
:*Choose Project type*: File based
:*Assign to team*: Assign this project to Python document translators
:*Select languages*: keep all languages listed (after choosing assign to team)

5. Once created, enter the settings of this newly created project to set up some more fields:

In *General* tab:

:Extended project description: If you want to translate Python documentation, you should follow the processes written on https://github.com/python-doc-ja/python-doc-ja/blob/master/README.md to apply yourself as a translator.
:Homepage: https://github.com/python-doc-ja/python-doc-ja
:Translator Instructions URL: https://github.com/python-doc-ja/python-doc-ja/wiki
:Tag: Python

In *Workflow* tab, enable the *Translation Memory Fillup* option by checking the checkbox;

    NOTE: The *Translation Memory Fillup* option is essential to have a translation in one of the version projects to be populated to this project. This drastically reduces translation effort replicating one contribution to other strings that are exactly the same.  

6. Adjust the `CI workflow <https://github.com/python-docs-translations/transifex-automations/tree/main/.github/workflows>`_ with the new Python version:

    #. Set ``PYTHON_NEWEST`` environment variable inside ``env`` to the new Python version
    #. Edit ``cpython_version`` inside ``strategy.matrix`` adding the new version to the beginning array

7. Push source strings to python-newest by manually running the CI workflow: Actions_ tab > CI > Run workflow button > "Branch: main" and confirm "Run workflow"

.. _Actions: https://github.com/python-docs-translations/transifex-automations/actions

8. Unlock translations in python-newest, if locked

9. Double-check resources in python-newest. New resources are named after their pot files (e.g. "3.11.pot"), and they should be renamed to match their slug (e.g. "whatsnew--3_11")

10. Announce that the maintenance is over, and that python-newest is now using new Python version
