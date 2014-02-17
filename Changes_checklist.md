## Before Merging into `master`
* Builds should not be broken
* Examples should be updated to reflect changes
* Documentation should be updated to reflect changes
* Update changelog in `docs` with changes
* If any changes have been made to `README.md`, ensure changes are mirrored to `README.rst` with `pandoc`

## Before Doing a Release
* Bump the version in `__init__.py`
* Publish a new release on GitHub
* Upload to PyPI

## After the Release
* Trigger a new documentation build on readthedocs
* Mark active the new version on RTD (or otherwise do any version management as necessary)
