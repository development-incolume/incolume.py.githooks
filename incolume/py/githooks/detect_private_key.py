"""Module check filenames."""

# ruff: noqa: T201

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

BLACKLIST: list[bytes] = [
    b'BEGIN RSA PRIVATE KEY',
    b'BEGIN DSA PRIVATE KEY',
    b'BEGIN EC PRIVATE KEY',
    b'BEGIN OPENSSH PRIVATE KEY',
    b'BEGIN PRIVATE KEY',
    b'PuTTY-User-Key-File-2',
    b'BEGIN SSH2 ENCRYPTED PRIVATE KEY',
    b'BEGIN PGP PRIVATE KEY BLOCK',
    b'BEGIN ENCRYPTED PRIVATE KEY',
    b'BEGIN OpenVPN Static key V1',
]


def has_private_key(*filenames: Sequence[Path]) -> bool:
    """Check if the content contains a private key.

    Args:
        filenames (Sequence[Path]): The sequence of file paths to check.

    """
    private_key_files = []

    for filename in filenames:
        with Path(filename).open('rb') as f:
            content = f.read().decode()
            if any(line in content for line in BLACKLIST):
                private_key_files.append(filename)

    if private_key_files:
        for private_key_file in private_key_files:
            print(f'Private key found: {private_key_file}')
        return False
    return True


def main(argv: Sequence[str] | None = None) -> int:
    """CLI to check private key.

    Args:
        argv (Sequence[str] | None, optional): _description_. Defaults to None.

    Returns:
        int: _description_

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    return has_private_key(args)


if __name__ == '__main__':
    raise SystemExit(main())
