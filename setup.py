import os
import sys
__DIR__ = os.path.abspath(os.path.dirname(__file__))
import codecs
from setuptools import setup
from setuptools.command.test import test as TestCommand
import tornado_json


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(__DIR__, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.md')


class Pytest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        # Using pytest rather than tox because Travis-CI has issues with tox
        # Import here, cause outside the eggs aren't loaded
        import pytest
        errcode = pytest.main(self.test_args)

        sys.exit(errcode)


setup(
    name="Tornado-JSON",
    version=tornado_json.__version__,
    url='https://github.com/hfaran/Tornado-JSON',
    license='MIT License',
    author='Hamza Faran',
    description=('A simple JSON API framework based on Tornado'),
    long_description=long_description,
    packages=['tornado_json'],
    install_requires = install_requires,
    tests_require=['pytest'],
    cmdclass = {'test': Pytest},
    data_files=[
        # Populate this with any files config files etc.
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)
