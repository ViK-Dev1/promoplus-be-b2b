# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Per indicare la directory dei sorgenti
import os, sys
sys.path.insert(0, os.path.abspath('../../AuthS/Code'))
sys.path.insert(0, os.path.abspath('../../AuthS/Code/Config'))
sys.path.insert(0, os.path.abspath('../../AuthS/Code/Database'))
sys.path.insert(0, os.path.abspath('../../AuthS/Code/BL'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Promo+ BE-B2B'
copyright = '2025, ViK'
author = 'ViK'
release = 'v.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo', 'sphinx.ext.autodoc', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = []
html_show_sourcelink = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_theme_options = {
    "light_logo": "logo_b.png",
    "dark_logo": "logo_w.png"
}
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
html_css_files = ["custom1.css"]

# Put this color in the furo.css file
'''
a:link, a:visited {
  color: #7bed9f !important;
}
7bed9f - day
05c46b - dark
'''


