"""Sphinx configuration."""
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# If extensions (or modules to document with autodoc) are in another
# directory, add these directories to sys.path here. If the directory is
# relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
#
import stimpool

# -- Project information -----------------------------------------------------

# General information about the project.
project = "stimpool"
copyright = "2021, Mario E. Bermonti Pérez"  # noqa: A001
author = "Mario E. Bermonti Pérez"
# The version info for the project you're documenting, acts as replacement
# for |version| and |release|, also used in various other places throughout
# the built documents.
#
# The short X.Y version.
version = stimpool.__version__
# The full version, including alpha/beta/rc tags.
release = stimpool.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",  # summary table
    "sphinx.ext.napoleon",  # write docstrings in numpy or google
    "recommonmark",
    "sphinx_markdown_tables",
    "sphinx.ext.coverage",
    "sphinx_autodoc_typehints",  # insert typehints into the final docs
    "sphinx_rtd_theme",
    "autodocsumm",  # generate summary of class attributes
]

# default for autodoc
autoclass_content = "both"
autodoc_member_order = "bysource"

# autodocsumm config
autodoc_default_options = {"autosummary": True}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
