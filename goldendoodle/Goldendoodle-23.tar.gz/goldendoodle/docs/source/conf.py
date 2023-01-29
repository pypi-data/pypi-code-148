# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import tomllib

sys.path.append(os.path.abspath('../../../'))
print(sys.path)

# The master toctree document.
master_doc = "index"

# -- Project information -----------------------------------------------------

with open("../../../pyproject.toml", "rb") as f:
    _toml_data = tomllib.load(f)
    project = ((_toml_data["tool"])["poetry"])["name"]
    author = (((_toml_data["tool"])["poetry"])["authors"])[0]
    copyright = str(datetime.datetime.now().date().year) + ', ' + author 
    version = ((_toml_data["tool"])["poetry"])["version"]

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
#    "linkify", FUTUREFEATURE
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_special_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_init_with_doc = True
# Report warnings for all validation checks
numpydoc_validation_checks = {"all"}