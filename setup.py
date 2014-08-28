 # -*- encoding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

assert sys.version_info >= (2, 7), "Python 2.7+ required."

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.rst')) as readme_file:
    with open(os.path.join(current_dir, 'CHANGES.rst')) as changes_file:
        long_description = readme_file.read() + '\n' + changes_file.read()

from tipboard import __version__

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

setup(
    name='tipboard',
    version=__version__,
    description='Tipboard - a flexible solution for creating your dashboards.',
    long_description = long_description,
    url='http://tipboard.allegrogroup.com',
    license='Apache Software License v2.0',
    author='Allegro Group and Contributors',
    author_email='pylabs@allegro.pl',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms=['any'],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'tipboard = tipboard.console:main',
        ],
    },
)
