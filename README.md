## Metadata
<!-- - Author: {author-profile-name}/{author-alias}. -->
- Name: '{project-name}'.
- Purpose: {short-description}.
- Format: {package-format}.
- License:
  - This project's license: [GNU General Public License v3.0](LICENSE)
  <!-- - Dependency-1: [{dependency-name}({license-1-name})] -->
  <!-- - Dependency-2: [{dependency-name}({license-2-name})] -->

## Setup
### Dependencies:
  - Version: __{python-version}__
  - Manager: [__{python-manager}__]({python-manager-link})
  <!-- [__pip__](https://docs.python.org/3/installing/index.html) -->
  <!-- [__poetry__](https://github.com/python-poetry/poetry) -->
  <!-- [__uv__](https://github.com/astral-sh/uv) -->
  - Toolset:
    - [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
    - [venv](https://docs.python.org/3/library/venv.html)
    - [pre-commit](https://github.com/pre-commit/pre-commit) (hooks)
        - [ruff](https://github.com/astral-sh/ruff)
        - [mypy](https://github.com/python/mypy)

### Installation:
{...}
<!-- Venv -->
  <!-- - Windows
    - `cd "C:\Users\{User}\AppData\Local\Programs\Python\Launcher"`
    - `.\py.exe -{python-version} -m venv "{path}/{project-name}/venv-{python-version}"` <sub>suggested</sub>
    - everything below
  - Linux
    - `python{python-version} -m venv {path}/{project-name}/{python-version}` <sub>suggested</sub>
    - everything below
  1. `cd {path}/{project-name}`
  2. `source venv-{python-version}/bin/activate`
  3. `pip install --upgrade pip`
  4. `pip install .`
  5. double check with `which python` (Linux) -->

### Usage:
  - project
    - {...}
  - local tests
    - {...}
    <!-- - `{project-name}/tests.py` -->
  - local CI
    <!-- - `pre-commit run --all-files` -->

## Example
### {example-1-title}
{...}