"""Hook to validate filenames."""

# ruff: noqa: T201
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

SNAKE_CASE_REGEX = re.compile('^[a-z_]+$')


def is_valid_filename(filename: str | Path, min_len: int = 3) -> bool:
    """Check if a filename is valid.

    A valid filename is in snake_case and has at least `min_len` characters.
    extract the name so that `/my/repo/x.py` becomes `x`
    """
    name = Path(filename).stem

    if too_short := len(name) < min_len:
        print(f'Name too short ({min_len=}): {filename}')

    if not_snake_case := SNAKE_CASE_REGEX.search(name) is None:
        print(f'Filename is not in snake_case: {filename}')

    failure = too_short or not_snake_case
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

    args = parser.parse_args(argv)

    results = [
        not is_valid_filename(filename, args.min_len)
        for filename in args.filenames
    ]
    return int(any(results))


if __name__ == '__main__':
    raise SystemExit(main())
