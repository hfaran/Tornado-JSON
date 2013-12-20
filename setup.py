from setuptools import setup
import tornado_json

with open("requirements.txt", "r") as f:
    install_requires = f.read().split()

setup(
    name="Tornado-JSON",
    version=tornado_json.__version__,
    author='Hamza Faran',
    author_email='hamza@hfaran.com',
    description=('A simple JSON API framework based on Tornado'),
    packages=['tornado_json'],
    install_requires = install_requires,
    data_files=[
        # Populate this with any files config files etc.
    ],
)
