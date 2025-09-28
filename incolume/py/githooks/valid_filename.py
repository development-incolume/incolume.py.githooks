"""Hook to validate filenames."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import TYPE_CHECKING

import rich
from icecream import ic

from incolume.py.githooks.utils import debug_enable

if TYPE_CHECKING:
    from collections.abc import Sequence

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


def main(argv: Sequence[str] | None = None) -> int:
    """Maint entry point for the script."""
    parser = argparse.ArgumentParser(
        prog='validate-filename',
    )
    parser.add_argument(
        'filenames',
        nargs='+',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--min-len',
        default=3,
        type=int,
        help='Minimum length for a filename.',
    )
    parser.add_argument(
        '--max-len',
        default=256,
        type=int,
        help='Maximum length for a filename.',
    )

    args = parser.parse_args(argv)

    results = [
        not is_valid_filename(
            filename=filename, min_len=args.min_len, max_len=args.max_len
        )
        for filename in args.filenames
    ]
    return int(any(results))


if __name__ == '__main__':
    raise SystemExit(main())
