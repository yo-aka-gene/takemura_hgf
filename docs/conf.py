# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import glob
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import tools

project = 'takemura_hgf'
copyright = '2023, Yuji Okano'
author = 'Yuji Okano'
version = tools.__version__
release = tools.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'nbsphinx', 'sphinx_gallery.load_style', 'myst_parser']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
htmlhelp_basename = 'takemura_hgf_doc'
html_logo = "_static/horizontal_logo.png"
html_theme_options = {"navigation_depth": 5, "logo_only": True}
master_doc = 'index'
latex_documents = [
    (master_doc, 'takemurahgf.tex',
     'takemura_hgf Analysis Details',
     'Yuji Okano', 'manual'),
]

man_pages = [
    (master_doc, 'takemura_hgf',
     'takemura_hgf Analysis Details',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'gbmseq',
     'takemura_hgf Analysis Details',
     author,
     'takemura_hgf',
     'HGF project',
     'Miscellaneous'),
]

nbsphinx_thumbnails = {
    "/".join(
        v.split(".")[:-1]
    ): v.replace(
        "jupyternb", "_static"
    ).replace(
        "ipynb", "png"
    ) if os.path.exists(
        v.replace(
            "jupyternb", "_static"
        ).replace(
            "ipynb", "png"
        )
    ) else "_static/logo.png" for v in glob.glob("jupyternb/*")
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
