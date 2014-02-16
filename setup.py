import os
import sys
# Temporary patch for issue reported here:
# https://groups.google.com/forum/#!topic/nose-users/fnJ-kAUbYHQ
import multiprocessing  # TODO: Remove when Travis-CI updates 2.7 to 2.7.4+
__DIR__ = os.path.abspath(os.path.dirname(__file__))
import codecs
from setuptools import setup
from setuptools.command.test import test as TestCommand
import tornado_json


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(__DIR__, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.rst')


class Tox(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        # self.test_args = []
        self.test_args = ['--verbose']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        # import tox
        # errcode = tox.cmdline(self.test_args)

        # Using pytest rather than tox because Travis-CI has issues with tox
        import pytest
        errcode = pytest.main(self.test_args)

        sys.exit(errcode)


setup(
    name="Tornado-JSON",
    version=tornado_json.__version__,
    url='https://github.com/hfaran/Tornado-JSON',
    license='MIT License',
    author='Hamza Faran',
    author_email='hamza@hfaran.com',
    description=('A simple JSON API framework based on Tornado'),
    long_description=long_description,
    packages=['tornado_json'],
    install_requires = install_requires,
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    data_files=[
        # Populate this with any files config files etc.
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)
