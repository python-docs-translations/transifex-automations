========================
Transifex administration
========================

These procedures are for administrators of the python-doc_ organization on
Transifex.

Recover a source resource with zero strings
-------------------------------------------

An upload can appear to succeed while leaving a Transifex resource with zero
strings. The source POT file may still be correct, but subsequent downloads of
that resource's translations produce broken PO files. For example, this happened to
``python-313.c-api--stable`` in `incident #246
<https://github.com/python-docs-translations/transifex-automations/issues/246#issuecomment-5663674024>`_.
The possible Transifex CLI upload bug is tracked in `transifex/cli#266
<https://github.com/transifex/cli/issues/266>`_.

To restore the source strings:

1. Check out the affected Python version branch of this repository (for
   example, ``3.13``). Confirm that its ``.tx/config`` maps the resource to a
   nonempty source POT file under ``pot/``. For the resource in incident #246,
   the source is ``pot/c-api/stable.pot``.
2. Install the :doc:`Transifex CLI <commands>` and set ``TX_TOKEN`` to an API
   token with permission to upload source strings. Only Transifex admins can
   push sources with ``-s``.
3. From the root of that branch, force-push the affected resource's source
   strings. For example:

   .. code-block:: shell

      tx push -f -s python-313.c-api--stable

4. Check that the resource on Transifex contains strings again. If broken PO
   files were downloaded while it was empty, pull translations again after
   restoring the source.

For configuring translation checks and custom placeholders, see the guide below.

.. toctree::
   :maxdepth: 1

   placeholders.rst

.. _python-doc: https://app.transifex.com/python-doc/
