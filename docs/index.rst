Python Docs Transifex Automations documentation
===============================================

For translators
---------------

If you are new to translating on Transifex_ please read our
:doc:`guide for new translators <new-translators>`.

For translation coordinators
----------------------------

In this documentation you can find guides for setting up and maintaining your
(Transifex enhanced) translation repository.

You can also find `Scripts <https://github.com/python-docs-translations/transifex-automation/tree/main/scripts>`_
and procedures for maintaining Python_ docs translation infrastructure
under the python-doc_ organization in Transifex_.

Source strings are updated using a continuous integration workflow under
`.github/workflows <https://github.com/python-docs-translations/transifex-automation/tree/main/.github/workflows>`_.
Details:

- Run weekly
- Run for releases in beta, release candidate, stable, bugfixes and security-fixes status; alpha or EOL are excluded;
- It **DOES NOT** store translations to be used by the published documentation;

See also  Translating_ in the Python Developer's Guide for more information.

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
