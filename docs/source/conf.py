# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


from api_compose.version import __version__

project = 'api-compose'
copyright = '2023, ken'
author = 'ken'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # create .rst files for source documnetation
    'sphinx.ext.autodoc',

    # Add doc support for pydantic models
    'sphinxcontrib.autodoc_pydantic',

    # Create [source] for method signature
    'sphinx.ext.viewcode',

    "nbsphinx",
    

    
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme ="pydata_sphinx_theme"
html_static_path = ['_static']
