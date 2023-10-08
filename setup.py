from distutils.util import convert_path
from pathlib import Path

from setuptools import setup, find_packages

from scripts.getters import get_version, get_cli, package_name

this_directory = Path(__file__).parent
long_description = this_directory.joinpath("README.rst").read_text()

if __name__ == '__main__':
    setup(
        name=package_name,
        version=get_version(),
        python_requires='>=3.9',
        description="A Framework for orchestrating, asserting and reporting on API calls with templates",
        long_description=long_description,
        long_description_content_type='text/x-rst',
        author="Ken",
        author_email="kenho811job@gmail.com",
        packages=find_packages("src"),
        package_dir={"": "src"},
        include_package_data=True,
        package_data={
            # Recursively include data files
            '': ['**/*.yaml', '**/*.j2', '**/*.rst', '**/*.py'],
        },

        # include all core templates and value files
        install_requires=[
            "requests==2.29.0",
            "jsonpath_ng==1.5.3",
            "typer[all]==0.9.0",
            "jinja2==3.1.2",
            "pyyaml==6.0",
            "pydantic==2.0.3",
            "pydantic-settings==2.0.3",
            "networkx==3.1",
            "python-dotenv==1.0.0",
            "matplotlib==3.7.2",
            "lxml==4.9.3",
            "cmd2==2.4.3",
            "jsonschema==4.19.0",

            # Demo Servers
            "connexion==2.14.2",
            "connexion[swagger-ui]",
            'dicttoxml==1.7.16',

        ],
        extras_require={
            "test": [
                "pytest==7.3.1",
                "pytest-env==1.0.1",
                'pydeps==1.12.8',
            ],
            "dist": [
                'twine==4.0.2',
            ],

            # For jupyter notebook tutorials
            "tutorials": [
                "jupyterlab",
                "jupyter-server-proxy==4.0.0",
            ],
        },
        entry_points={
            'console_scripts': [
                f'{get_cli()}=api_compose.cli.main:app',
            ],
        },
    )
