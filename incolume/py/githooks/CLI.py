"""Module Command Line Inteface."""

from __future__ import annotations

import argparse
from typing import TYPE_CHECKING

from incolume.py.githooks.valid_filename import is_valid_filename

if TYPE_CHECKING:
    from collections.abc import Sequence


def check_valid_filenames_cli(argv: Sequence[str] | None = None) -> int:
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
    raise SystemExit(check_valid_filenames_cli())
