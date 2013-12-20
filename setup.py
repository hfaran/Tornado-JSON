import os
import sys
__DIR__ = os.path.abspath(os.path.dirname(__file__))
import codecs
from setuptools import setup
import tornado_json


if not sys.version_info[:2] == (2, 7):
    print "Sorry, only Python2.7 is supported."
    exit()


def read(filename):
    """Read and return `filename` in root dir of project and return string"""
    return codecs.open(os.path.join(__DIR__, filename), 'r').read()


install_requires = read("requirements.txt").split()
long_description = read('README.rst')


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
