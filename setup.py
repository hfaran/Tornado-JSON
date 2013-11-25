from setuptools import setup

setup(
    name="touchpoint",
    version='0.1',
    author='Hamza Faran',  # Add other authors/remove?
    author_email='hamza@hfaran.com',  # Add other authors/remove?
    description=('Touchpoint Web App'),
    packages=['touchpoint'],
    install_requires = [
        # Populate this with packages from requirements.txt
    ],
    data_files=[
        # Populate this with any files config files etc.
    ],
    entry_points={
        'console_scripts': ['touchpoint = touchpoint.main:main']
    }
)
