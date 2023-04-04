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

html_favicon = "_static/pyzeal_favicon.ico"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
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

bibtex_bibfiles = ["refs.bib"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_material"
# Set link name generated in the top bar.
html_title = "Python ZEros of AnaLytic Functions"

# Material theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the navigation.
    "nav_title": "The PyZEAL Project",
    # Set the color and the accent color
    "color_primary": "blue-grey",
    "color_accent": "green",
    # Set the repo location to get a badge with stats
    "repo_url": "https://github.com/Spectral-Analysis-UPB/PyZEAL",
    "repo_name": "PyZEAL",
    # 'logo_icon': '&#xeba5',
}

# html_logo = '_static/rocket.svg'

html_sidebars = {
    "**": [
        "logo-text.html",
        "globaltoc.html",
        "localtoc.html",
        "searchbox.html",
    ]
}
# html_theme = 'classic'
# html_theme_options = {
#     "relbarbgcolor": "green",
#     "footerbgcolor": "black",
#     "body_min_width": "60%",
#     "body_max_width": "70%"
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
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
