# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Python Docs Transifex Automations'
copyright = '2025, rffontenelle'
author = 'rffontenelle'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = 'Python Docs Transifex Automations'

# ----------------------------------------------------------------------------

# Python versions
newest = '3.13'
previous = '3.12'

rst_prolog = f"""
.. |py_new| replace:: {newest}
.. |py_last| replace:: {previous}
"""
