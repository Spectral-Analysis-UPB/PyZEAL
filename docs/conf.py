# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import importlib.metadata

# -- Project information -----------------------------------------------------

project = "PyZEAL"
copyright = "2022, Philipp Schuette"
author = "Philipp Schuette"

# The short X.Y version
version = importlib.metadata.version("pyzeal")
# The full version, including alpha/beta/rc tags
release = importlib.metadata.version("pyzeal")

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "nbsphinx",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.bibtex",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

bibtex_bibfiles = ["./_static/refs.bib"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "misc/intro.rst", "misc/badges.rst"]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_material"
html_favicon = "_static/pyzeal_favicon.ico"
html_short_title = "Python ZEros of AnaLytic Functions"
html_title = "PyZEAL"

# Material theme options (see theme.conf for more information)
html_theme_options = {
    "nav_title": "The PyZEAL Project",
    "color_primary": "blue-grey",
    "color_accent": "green",
    "repo_url": "https://github.com/Spectral-Analysis-UPB/PyZEAL",
    "repo_name": "PyZEAL",
    # "version_dropdown": True,
    "globaltoc_depth": 3,
    "globaltoc_collapse": True,
    # "logo_icon": "&#xf8ee",
}

# html_logo = "_static/images/resonance_example.png"

html_sidebars = {
    "**": [
        "logo-text.html",
        "globaltoc.html",
        "localtoc.html",
        "searchbox.html",
    ]
}

html_domain_indices = True

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]

# the name of the syntax highlighting style to use
pygments_style = "emacs"

# Add type of source files
source_suffix = [".rst"]

autodoc_typehints = "signature"
typehints_defaults = "braces-after"
typehints_document_rtype = True
typehints_use_rtype = False
