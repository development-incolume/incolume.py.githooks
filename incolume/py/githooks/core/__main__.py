"""Module core.__main__ for project."""

from __future__ import annotations

import logging
from contextlib import suppress
from os import getenv
from pathlib import Path

from icecream import ic

ic.disable()

with suppress(ImportError, ModuleNotFoundError):
    import tomllib as tomli

with suppress(ImportError, ModuleNotFoundError):
    import tomli


confproject = Path(__file__).parents[4] / 'pyproject.toml'
fileversion = Path(__file__).parents[1] / 'version.txt'

with suppress(FileNotFoundError), confproject.open('rb') as f:
    fileversion.write_text(
        f'{tomli.load(f)["project"]["version"]!s}\n',
    )

__version__ = fileversion.read_text().strip()
__package_name__ = 'incolume.py.githooks'


def debug_var_active() -> bool:
    """Check environment variables for debug mode."""
    debug: bool = any(
        getenv(x, '').casefold() in {'1', 'true', 'on'}
        for x in ('INCOLUME_DEBUG_MODE', 'DEBUG_MODE', 'DEBUG')
    )

    msg: str = f'Debug mode {"enabled" if debug else "disabled"}.'
    ic(msg)
    logging.debug(msg=msg)

    return debug


def debug_enable() -> bool:
    """Enable debug mode."""
    debug: bool = debug_var_active()
    ic.disable()  # Disable by default

    if debug:
        ic.enable()
    return debug


debug_enable()  # Enable debug mode if environment variable is set
