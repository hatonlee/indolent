# indolent

[![Changelog](https://img.shields.io/badge/changelog-C3B091?style=for-the-badge)](/docs/CHANGELOG.md)
[![Requirements](https://img.shields.io/badge/requirements-C3B091?style=for-the-badge)](/docs/requirements.md)
[![Architecture](https://img.shields.io/badge/architecture-C3B091?style=for-the-badge)](/docs/architecture.md)
[![Time Tracking](https://img.shields.io/badge/time%20tracking-C3B091?style=for-the-badge)](/docs/timetracking.md)
[![AI Usage](https://img.shields.io/badge/ai%20usage-C3B091?style=for-the-badge)](/docs/ai.md) <br>
![GitHub Release](https://img.shields.io/github/v/release/hatonlee/indolent?include_prereleases&style=for-the-badge)
[![License](https://img.shields.io/github/license/hatonlee/indolent?style=for-the-badge)](LICENSE)
![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fohtu-ryhma1%2Foutin-bib%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&style=for-the-badge) <br>
[![Code style: black](https://img.shields.io/badge/code%20style-black-black?style=for-the-badge)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-1674b1?style=for-the-badge)](https://pycqa.github.io/isort/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen?style=for-the-badge)](https://github.com/pylint-dev/pylint)

indolent is a python app for tracking habits. Currently habits can be created with a name and a description.

## Instructions

### Installation
1. Install [Poetry](https://python-poetry.org/)
2. Clone the repository `git clone https://github.com/hatonlee/indolent.git`
3. Run `poetry install`

### Usage
1. Start the app: `poetry run invoke start`

### Testing
- Run unit tests and coverage: `poetry run invoke coverage`
- Create a coverage report: `poetry run invoke coverage-report`
- Run pylint: `poetry run invoke lint`
- Format using black and isort: `poetry run invoke coverage-report`
