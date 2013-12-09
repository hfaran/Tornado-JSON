from setuptools import setup

setup(
    name="Tornado-JSON",
    version='0.1',
    author='Hamza Faran',
    author_email='hamza@hfaran.com',
    description=('A simple JSON API framework based on Tornado'),
    packages=['tornado_json'],
    install_requires = [
        "MySQL-python",
        "tornado",
        "dataset",
        "torndb",
        "jsonschema",
    ],
    data_files=[
        # Populate this with any files config files etc.
    ],
)
