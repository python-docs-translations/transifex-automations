================
Sample Workflows
================

All Python documentation translation repositories are hosted on `GitHub <https://github.com>`_.
GitHub provides a very useful `CI <https://en.wikipedia.org/wiki/Continuous_integration>`_
system, *GitHub Actions*, which runs *workflows*. Workflows are particularly useful
for testing projects, in translation repos they can be used to update translations
from Transifex, lint translated files, and test build the translated documentation.

This repository provides three sample workflows: a Linting workflow, a Test Build
workflow, and a workflow for pulling translations from Transifex. They can be found
in the `sample-workflows <https://github.com/python-docs-translations/transifex-automations/tree/main/sample-workflows>`_
directory and explanations of how they work and what you need to do to set them up can be found below.

.. seealso::
   - `GitHub docs: Writing workflows <https://docs.github.com/en/actions/writing-workflows>`_
   - :doc:`Setting up Transifex <commands>`

Running Workflows
-----------------

To run on of our provided workflows (or any workflow), put the file in the
``.github/workflows`` folder and it will run automatically depending on how it
is configured.

General Overview
----------------

.. code-block:: yaml

   name: Linting Workflow

The name can be freely configured and will be displayed in the "Actions" tab.

.. code-block:: yaml

   on:
      schedule:
         - cron: '0 0 * * *'

Using `cron <https://en.wikipedia.org/wiki/Cron>`_, the frequency of the workflow
runs can be set. In the sample workflows it is configured to ``'0 0 * * *'``,
meaning it will run once daily. See `crontab.guru <https://crontab.guru/>`_ for
a simple cron editor.

.. code-block:: yaml

   on:
      ...
      push:
         branches:
            - '*'
      workflow_dispatch:

The workflow can also be set to run under different conditions, in the case of the
sample workflows it is set to run on a ``push`` to any branch, and can be run
manually due to the ``workflow_dispatch`` option.

.. code-block:: yaml

   jobs:

All jobs or sections under ``jobs:`` will be run. The sample workflows can be
merged into one by combining all of their jobs. (Note: there must only be one `jobs:`)

.. important::

    In the workflows, replace all instances of ``XX`` with your `IETF <https://datatracker.ietf.org/doc/html/rfc5646.html>`_
    language tag, as described in `PEP 545 <https://peps.python.org/pep-0545/#language-tag>`_.
    These tools, however, require and underscore (``_``) rather than a dash (``-``);
    for example ``pl`` or ``pt_BR``.


Transifex Pull Workflow
-----------------------

How to configure the `Transifex Pull Workflow <https://github.com/python-docs-translations/transifex-automations/blob/main/sample-workflows/transifex-pull.yml>`_.

This workflow automatically pulls updated translations from Transifex, commits
them to the repository, and pushes them back to the relevant branch, if
significant changes are detected.

Ensure the ``TX_TOKEN`` secret is configured in your repository with your Transifex API token.
For generating your API key, see this `Transifex article <https://help.transifex.com/en/articles/6248858-generating-an-api-token>`_,
for setting up secrets, see this `guide <https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions#creating-secrets-for-a-repository>`_.

.. code-block:: yaml

     matrix:
       version: [ 3.14 ]

Set the ``version`` list to the branches for which translations should be updated.

.. code-block:: yaml

   - name: Filter files
     run: |
       ! git diff -I'^"POT-Creation-Date: ' \
                  -I'^"Language-Team: ' \
                  -I'^# ' -I'^"Last-Translator: ' \
                  --exit-code \
         && echo "SIGNIFICANT_CHANGES=1" >> $GITHUB_ENV || exit 0

This step detects whether the changes are significant by ignoring changes
to the file header. A commit and push only occur if meaningful changes are found,
these filters can be modified to suit.

The workflow pulls translations using the `Transifex CLI <https://developers.transifex.com/docs/cli>`_
and is currently configured to pull *all* files. The configuration options
can be modified with the command line argument ``--pull-options``, for example:

.. code-block::

    --pull-options="--mode reviewed" # This will only pull reviewed translations


Test Build Workflow
-------------------

How to configure the `Test Build Workflow <https://github.com/python-docs-translations/transifex-automations/blob/main/sample-workflows/test-build.yml>`_.

.. code-block:: yaml

         matrix:
            version: [ 3.14 ]
            format: [ html, latex ]

Set version to the branches in your translation repository that you want to be
built, for example: ``version: [ 3.14, 3.13, 3.12 ]``, note that this has to be
changed in both ``matrix``'s in the workflow. The format can be modified
to run for just ``html`` if that is preferred.

.. code-block:: yaml

         - uses: actions/setup-python@master
            with:
            python-version: 3.12  # pin for Sphinx 3.4.3 for 3.10

The ``python-version`` can be unpinned if no branches older than ``3.11`` are set
in the ``version`` list.

.. code-block:: yaml

      output-pdf:

Remove the ``output-pdf`` job if you do not want pdf output to be built. The
section also has to be removed if ``latex`` is not in the ``format`` list.

The workflow uses the ``actions/upload-artifact@master`` tool which allows for
the generated builds to be downloaded. In a run in the "Actions" tab they can be
found in the "Artifacts" section.


Linting Workflow
----------------

How to configure the po linting `workflow <https://github.com/python-docs-translations/transifex-automations/blob/main/sample-workflows/po-lint.yml>`_.
This workflow will lint all po files on your branch using `sphinx-lint <https://pypi.org/project/sphinx-lint/>`_.

.. code-block:: yaml

      matrix:
         version: [ 3.14 ]

Set the ``version`` list to the versions you have available and want the linting
workflow to be run on.
