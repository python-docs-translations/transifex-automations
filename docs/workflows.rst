================
GitHub Workflows
================

All Python documentation translation repositories are hosted on `GitHub <https://github.com>`_.
GitHub provides a very useful `CI <https://en.wikipedia.org/wiki/Continuous_integration>`_
system, *GitHub Actions*, which runs *workflows*. Workflows are particularly useful
for testing projects, in translation repos they can be used to update translations
from Transifex, lint translated files, and test build the translated documentation.

This repository provides three sample workflows, a Linting workflow, a Test Build
workflow, and a workflow for pulling translations from Transifex. They can be found
in the `FOLDER <https://github.com>`_ and explanations of how they work and what
you need to do to set them up can be found below.

.. seealso::
   - `GitHub docs: Writing workflows <https://docs.github.com/en/actions/writing-workflows>`_
   - :doc:`Setting up Transifex <commands.rst>`

Running Workflows
-----------------

To run on of our provided workflows (or any workflow), put the file in the
``.github/workflows`` folder and it will run automatically depending on how it
is configured.

General Overview
----------------

.. code-block:: workflow

   name: Linting Workflow

The name can be freely configured and will be displayed in the "Actions" tab.

.. code-block:: workflow

   on:
      schedule:
         - cron: '0 * * * *'

Using `cron <https://en.wikipedia.org/wiki/Cron>`_, the frequency the workflow
runs can be set. In the sample workflows it is configured to ``'0 * * * *'``,
this means it will run hourly.

.. code-block:: workflow

   on:
      ...
      push:
         branches:
            - '*'
      workflow_dispatch:

The workflow can also be set to run under different conditions, in the case of the
sample workflows it is set to run on a ``push`` to any branch, and can be run
manually due to the ``workflow_dispatch`` option.

.. code-block:: workflow

   jobs:

All jobs or sections under ``jobs:`` will be run. The sample workflows can be
merged into one by combining all of their jobs. (Note there must only be one `jobs:`)

.. Transifex Pull Workflow
.. -----------------------
..
.. This workflow pulls all translations from transifex.

Test Build Workflow
-------------------

How to configure the `Test Build Workflow <https://github.com>`_.

In the workflow replace all instances of ``XX`` with your ITFL language code.

.. code-block:: workflow

         matrix:
            version: [ 3.13 ]
            format: [ html, latex ]

Set version to the branches in your translation repository that you want to be
built, for example: ``version: [ 3.13, 3.12, 3.11 ]``, note that this has to be
changed in both ``matrix``'s in the workflow. The format can be modified
to run for just ``html`` if that is preferred.

.. code-block:: workflow

         - uses: actions/setup-python@master
            with:
            python-version: 3.12  # pin for Sphinx 3.4.3 for 3.10

The ``python-version`` can be unpinned if no branches older than ``3.11`` are set
in the ``version`` list.

.. code-block:: workflow

      output-pdf:

Remove the ``output-pdf`` job if you do not want pdf output to be built. The
section also has to be removed if ``latex`` is not in the ``format`` list.

The workflow uses the ``actions/upload-artifact@master`` tool which allows for
the generated builds to be downloaded. In a run in the "Actions" tab they can be
found in the "Artefacts" section.


Linting Workflow
----------------

This workflow will lint all po files on your branch using `sphinx-lint <https://pypi.org/project/sphinx-lint/0.4/>`_.

.. code-block:: workflow

      matrix:
         version: [ 3.13 ]

Set the ``version`` list to the versions you have available and want the linting
workflow to be run on.
