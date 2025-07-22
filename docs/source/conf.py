import os
import sys
sys.path.insert(0, os.path.abspath("../.."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EMDB API client'
copyright = '2025, Neli Fonseca'
author = 'Neli Fonseca'
release = '0.1.7'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # optional, for Google/NumPy style (you can keep it)
    "sphinx.ext.viewcode",  # optional, adds links to source code
]

templates_path = ['_templates']
exclude_patterns = []

autodoc_member_order = "groupwise"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
