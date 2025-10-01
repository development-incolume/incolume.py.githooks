"""Hook to validate filenames."""

from __future__ import annotations

import re
from pathlib import Path

from icecream import ic

from incolume.py.githooks.utils import Result, debug_enable

debug_enable()

SNAKE_CASE_REGEX = re.compile(r'^[a-z_][a-z_0-9]+$')


def is_valid_filename(
    filename: str | Path, min_len: int = 3, max_len: int = 256
) -> Result:
    """Check if a filename is valid.

    A valid filename is in snake_case and has at least `min_len` characters.
    extract the name so that `/my/repo/x.py` becomes `x`
    """
    msg_return = ''
    name = Path(filename).stem
    refname = re.sub(r'[^a-z0-9]', '', name)
    ic(name, len(name), refname, len(refname), min_len, max_len)

    if too_short := len(refname) < min_len:
        msg_return += f'\n[red]Name too short ({min_len=}): {filename}[/]'

    if too_long := len(refname) > max_len:
        msg_return += f'\n[red]Name too long ({max_len=}): {filename}[/]'

    if not_snake_case := SNAKE_CASE_REGEX.search(name) is None:
        msg_return += f'\n[red]Filename is not in snake_case: {filename}[/]'

    failure = (too_short or too_long) or not_snake_case
    return Result(code=not failure, message=msg_return)
