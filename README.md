<img title="Logo incolume.py.githooks" alt="logo incolume.py.githooks" src="assets/png/incolume-py-githooks.png" width=150 style="display: block; margin: 0 auto; width: 150;">

# incolume.py.githooks
<!--
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/incolume.py.githooks?color=00FFFF)
![PyPI - Version](https://img.shields.io/pypi/v/incolume.py.githooks?color=00FFFF&label=pypi+package)
-->
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

---

Hooks git for incolume projects.

## Usage

### Configuration

Model for .pre-commit-config.yaml, bellow:

```yaml
# File .pre-commit-config.yaml

default_install_hook_types: [pre-commit, prepare-commit-msg]
repos:

- repo: https://github.com/pre-commit/pre-commit-hooks
  # See https://pre-commit.com for more information
  # See https://pre-commit.com/hooks.html for more hooks  rev: v6.0.0
  hooks:
    - id: check-added-large-files
    - id: check-ast
    - id: check-case-conflict
    - id: check-docstring-first
    - id: check-illegal-windows-names
    - id: check-json
    - id: check-toml
    - id: check-xml
    - id: check-yaml
    - id: detect-private-key
    - id: double-quote-string-fixer
    - id: end-of-file-fixer
    - id: forbid-new-submodules
    - id: forbid-submodules
    - id: name-tests-test
    - id: no-commit-to-branch
    - id: pretty-format-json
    - id: trailing-whitespace

- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.13.0
  hooks:
    # Run the linter.
    - id: ruff-check
      args: [--config, ruff.toml, --fix ]
    # Run the formatter.
    - id: ruff-format
      args: [--config, ruff.toml]

- repo: https://github.com/development-incolume/incolume.py.githooks
  # https://github.com/development-incolume/incolume.py.githooks/blob/dev/README.md
  rev: 1.8.0
  hooks:
    - id: check-len-first-line
    - id: check-precommit-installed
    - id: check-valid-branchnames
    - id: check-valid-filenames
    #   args: ['--min-len=3', '--max-len=256']
    - id: detect-key
    - id: effort-message
    - id: footer-signed-off-by
    #   args: [--signoff]
    - id: insert-diff-commit
    - id: validate-message-commit


```
