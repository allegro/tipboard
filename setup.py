import pathlib, sys
from setuptools import setup, find_packages

assert sys.version_info >= (3, 7), "Python 3.7+ required."

# The directory containing this file
HERE = pathlib.Path.cwd()


# The text of the README file
README = (HERE / "README.md").read_text()

print(README)

with open(HERE / 'requirements.txt') as requirements:
    required = requirements.read().splitlines()

from src import __version__

setup(
    name="tipboard2.0",
    version=__version__,
    description="Tipboard - a flexible solution for creating your dashboards.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="http://tipboard.allegrogroup.com",
    author="Allegro Group and Contributors",
    author_email="pylabs@allegro.pl",
    license='Apache Software License v2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        'console_scripts': [
            'tipboard = src.manage:main_as_pkg',
        ],
    },
)


