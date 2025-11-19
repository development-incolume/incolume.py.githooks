"""Module githooks."""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path

from incolume.py.githooks.core import debug_enable

with suppress(ImportError, ModuleNotFoundError):
    import tomllib as tomli  # type: ignore[import]

with suppress(ImportError, ModuleNotFoundError):
    import tomli  # type: ignore[import]

debug_enable()

confproject = Path(__file__).parents[3] / 'pyproject.toml'
fileversion = Path(__file__).parent / 'version.txt'

with suppress(FileNotFoundError), confproject.open('rb') as f:
    fileversion.write_text(
        f'{tomli.load(f)["project"]["version"]!s}\n',
    )

__version__ = fileversion.read_text().strip()
