import os
import re
import codecs

from setuptools import setup

# Single source the version
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pypipackagemanagement',
    version=find_version("src", "pypipackagemanagement", "__init__.py"),
    packages=['pypipackagemanagement'],
    package_dir={'': 'src'},
    install_requires=['packaging'],
    url='https://github.com/hsorby/pypipackagemanagement',
    license='APACHE License',
    author='Hugh Sorby',
    author_email='h.sorby@auckland.ac.nz',
    description='A package for managing and bumping versions of packages on PyPi.'
)
