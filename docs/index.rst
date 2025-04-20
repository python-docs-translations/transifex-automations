Python Docs Transifex Translations documentation
================================================

Scripts and procedures for maintaining Python_ documentation translation infrastructure under python-doc_ organization in Transifex_.

Source strings are updated using continuous integration workflow under *.github/workflows*. Details:

- Run weekly
- Run for releases in beta, release candidate, stable, bugfixes and security-fixes status; alpha or EOL are excluded;
- It DOES NOT store translations to be used by the published documentation;

See docs_ directory for more information on this project maintenance.

See Translating_ in Python Developer's Guide for more information.

.. _Python: https://www.python.org
.. _python-doc: https://app.transifex.com/python-doc/
.. _Transifex: https://www.transifex.com
.. _docs: https://github.com/python-docs-translations/transifex-automations/blob/main/docs/
.. _Translating: https://devguide.python.org/documentation/translating/

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   new-translators.rst
   bumping-relsease.rst
   commands.rst
   placeholders.rst

