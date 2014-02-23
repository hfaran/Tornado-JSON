## Before Merging into `master`
* Builds should not be broken
* Examples should be updated to reflect changes
* Documentation should be updated to reflect changes
* If any changes have been made to `README.md`, ensure changes are mirrored to `README.rst` with `pandoc`

## Before Doing a Release
* Update changelog in `docs` with changes
* Bump the version in `__init__.py`
* Publish a [new release on GitHub](https://github.com/hfaran/Tornado-JSON/releases)
* Upload to [PyPI](https://pypi.python.org/pypi/Tornado-JSON)

## After the Release
* Trigger a new documentation build on [readthedocs](https://readthedocs.org/projects/tornado-json/)
* Mark active the new version on RTD (or otherwise do any version management as necessary)
