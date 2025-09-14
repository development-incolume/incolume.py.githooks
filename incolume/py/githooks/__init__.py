"""Module githooks."""

import contextlib
import importlib.metadata
import re
from pathlib import Path
from typing import Final

import tomllib as tomli

REGEX_SEMVER: Final = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
confproject = Path(__file__).parents[3] / 'pyproject.toml'
fileversion = Path(__file__).parent / 'version.txt'

with contextlib.suppress(FileNotFoundError), confproject.open('rb') as f:
    fileversion.write_text(
        f'{tomli.load(f)["project"]["version"]!s}\n',
    )

__version__ = fileversion.read_text().strip()
