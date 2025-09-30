"""Hook to validate filenames."""

from __future__ import annotations

import re
from pathlib import Path

import rich
from icecream import ic

from incolume.py.githooks.utils import debug_enable

debug_enable()

SNAKE_CASE_REGEX = re.compile(r'^[a-z_][a-z_0-9]+$')


def is_valid_filename(
    filename: str | Path, min_len: int = 3, max_len: int = 256
) -> bool:
    """Check if a filename is valid.

    A valid filename is in snake_case and has at least `min_len` characters.
    extract the name so that `/my/repo/x.py` becomes `x`
    """
    name = Path(filename).stem
    refname = re.sub(r'[^a-z0-9]', '', name)
    ic(name, len(name), refname, len(refname), min_len, max_len)

    if too_short := len(refname) < min_len:
        rich.print(f'[red]Name too short ({min_len=}): {filename}[/]')

    if too_long := len(refname) > max_len:
        rich.print(f'[red]Name too long ({max_len=}): {filename}[/]')

    if not_snake_case := SNAKE_CASE_REGEX.search(name) is None:
        rich.print(f'[red]Filename is not in snake_case: {filename}[/]')

    failure = (too_short or too_long) or not_snake_case
    return not failure
