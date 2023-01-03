# Developpement

## Conventions

Referer to <https://docs.python-guide.org/writing/style/#conventions>

## Visual Studio setup

- ms-python.python
- njpwerner.autodocstring
- LittleFoxTeam.vscode-python-test-adapter

## Other trick (only for dev mode)

### Disabling Bytecode (.pyc) Files

Source : <https://python-guide.readthedocs.io/en/latest/writing/gotchas/#bytecode-pyc-files-everywhere>

```sh
export PYTHONDONTWRITEBYTECODE=1
find . -type f -name "*.py[co]" -delete -or -type d -name "__pycache__" -delete
```

## Setup environnement

```sh
python -m pip install virtenv
python -m virtenv devenv
source devenv/bin/activate # or devenv/Scripts/activate from windows (via git bash with visualstudio)
python -m pip install -r requirements.txt
```

## Lint validation

Use flake8 tool for lint

- Ignore E501 : line too long

Execute linter

```sh
python -m pip install flake8
flake8 qakcentreon
```

## Unit test

Tests use unittest format.

Execute unit tests :

```sh
python -m unittest discover -s tests
```

## Tests coverage

```sh
python -m pip install coverage
python -m coverage run --source qakcentreon -m unittest discover -s tests
python -m coverage report
python -m coverage report -m # Show missing part of code
```

## Setup and update requirements file

```sh
python -m pip install pipreqs
pipreqs qakcentreon
```

```sh
python -m pip list --outdated
```
