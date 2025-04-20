==============================================================================
Guidance for New Contributors to Python Documentation Translation on Transifex
==============================================================================

This guide is intended for language teams working on the Python documentation
within the python-doc_ organization on Transifex_. Yes: not all teams translate
on Transifex, so using Transifex is optional.

.. _python-doc: https://app.transifex.com/python-doc
.. _Transifex: https://www.transifex.com/


Getting Started with Python Documentation Translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure that translations are of a good standard, it is essential that you are
confident in both English and the translation language.

If you are new to the translation of Python documentation, we recommend that
you start by reading the Translating_ on `Python Developer's Guide`_
(a.k.a. devguide), joining the relevant contact channels, and familiarizing
yourself with `PEP 545`_.

If there is already a repository for your language team, please join and
introduce yourself to the team.

**If there is no existing repository or language team, you will need to create
one.** Simply translating on Transifex is not enough to have your language
published in the Python documentation. Please follow the instructions on starting
a new translation.

.. _Translating: https://devguide.python.org/documentation/translating/
.. _Python Developer's Guide: https://devguide.python.org
.. _PEP 545: https://peps.python.org/pep-0545/


Geting to Know Transifex
~~~~~~~~~~~~~~~~~~~~~~~~

If you are new to Transifex, it is recommended that you take the time to read
through the following resources from the Transifex documentation:

- `Getting started as a translator <https://help.transifex.com/en/articles/6248698-getting-started-as-a-translator>`_: This covers signing up for an account and joining translation team.
- `Translating with the Web Editor <https://help.transifex.com/en/articles/6318216-translating-with-the-web-editor>`_: This covers getting to the editor, searching and filtering strings, and translating strings.
- `Other Tools in the Editor <https://help.transifex.com/en/articles/6318944-other-tools-in-the-editor>`_: This covers the history, glossary, comments, keyboard shortcuts, and more.
- `Starting with the basics <https://help.transifex.com/en/collections/3441044-starting-with-the-basics>`_: A group of documents with basic information.


Transifex Does Not Update docs.python.org
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Language teams must download and store the translation files in their VCS
repository, as per instructions from Translating_ on `Python Developer's Guide`_,
as it is from this repository that the python-docs infrastructure will fetch
translations, build the translated docs, and publish them on docs.python.org.

Projects within python-doc
~~~~~~~~~~~~~~~~~~~~~~~~~~

The python-doc_ organization contains several projects, each representing the
documentation for a specific version of Python (e.g. 3.11). The "Python" project
(slug "python-newest") is the latest version available for translation. All other
projects are named "Python <version>".


The Latest Version for Translation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "Python" project in Transifex always contains the latest stable release of
Python or its latest beta/RC release, but not alpha releases. For example, if
the latest version is 3.12, the "Python" project will only be updated with
strings from the 3.13 branch when a beta is released.


Translate the Latest Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Translations are propagated across projects for the same string, meaning that
you only need to translate once and all versions of the Python documentation
will receive the contribution *if the string remains unchanged*. If a string has
changed between versions, the contribution will not be applied to the new version.

It is recommended to focus your translation efforts on the "Python" project,
which represents the newest version. Keep in mind that the Python documentation
contains a large number of strings and that translations will be propagated, so
older versions will receive most contributions. Additionally, translating the
newest version is more important as it will have fewer differences from the source
string and receive more contributions.


Placeholders
~~~~~~~~~~~~

When translating in Transifex, you will encounter strings with `custom
placeholders <placeholders.rst>`_ in the form of Sphinx roles (e.g. \:class:\`turtle`).
These placeholders help highlight the role of specific elements, making it easier to
translate them correctly and avoid warnings from Transifex if they are translated incorrectly.

For instance, if the source string contains ``:class:`turtle```, the translation
string should also include the same placeholder. If it's missing, Transifex will
display a warning message.

Occasionally, you may encounter false-positives in the warnings. It is important
to check these warnings before ignoring them to ensure accuracy.

Final words
~~~~~~~~~~~

It is recommended that you also follow the style guide for your language and
review any existing translations to understand the tone and style of the language
team. Translating the Python documentation can be a large project, and contributions
from many members of the community are appreciated. If you need help or have
questions, please reach out to the language team or any other contact channel
provided in Translating_ on `Python Developer's Guide`_, or contact the
python-doc project coordinators on Transifex.

See also
~~~~~~~~

- PEP 545: https://peps.python.org/pep-0545/
- Translating: https://devguide.python.org/documentation/translating/
- Sphinx's reStructuredText Primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
