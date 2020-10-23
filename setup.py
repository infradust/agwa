import os
import sys
from setuptools import setup, find_packages
from aglabler import __version__


# required for building/installing from local sdist (.tar.gz) file
here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
tests_require = [
    'pytest',
    'pytest-runner',
    'pytest-mock',
    'mock']
pytest_runner = tests_require if needs_pytest else []

setup_requires = pytest_runner

install_requires = [
    'boto3'
]


setup(
    name="aglabler",
    version=__version__,
    author="Dan Shelly",
    author_email="danshelly@gmail.com",
    description="Agwa home task",
    python_requires='>=3.7',
    setup_requires=setup_requires,
    extras_require={'dev': tests_require},
    tests_require=tests_require,
    install_requires=install_requires,
    packages=find_packages(exclude=['docs', 'tests', 'scripts'])
)

