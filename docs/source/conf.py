# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'TextEditor'
copyright = '2026, Joe Rittiner'
author = 'Joe Rittiner'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../tests'))

extensions = [
    'sphinx.ext.napoleon',  # Allows NumPy style docstrings
    'sphinx_needs',
    'sphinxcontrib.plantuml',
]

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

needs_id_regex = r"^[A-Z0-9-]{3,}"
needs_id_length = 3

needs_types = [
    dict(directive="inv", title="Invariant", prefix="INV-", style="node"),
    dict(directive="freq", title="Requirement", prefix="FR-", style="node"),
    dict(directive="nfreq", title="Non-Functional Requirement", prefix="NFR-", style="node"),
    dict(directive="nreq", title="Non-Requirement", prefix="NR-", style="node"),
]
