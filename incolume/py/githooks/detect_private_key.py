"""Module check filenames."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from icecream import ic

from incolume.py.githooks.core import Result, debug_enable
from incolume.py.githooks.rules import Status

if TYPE_CHECKING:
    from collections.abc import Sequence

debug_enable()

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


def has_private_key(*filenames: Sequence[Path]) -> Result:
    """Check if the content contains a private key.

    Args:
        filenames (Sequence[Path]): The sequence of file paths to check.

    """
    private_key_files = []
    result = Result(code=Status.SUCCESS, message='')
    logging.debug(ic(filenames))

    for filename in filenames:
        logging.info(ic(filename))
        with Path(filename).open('rb') as f:
            content = f.read()
            if any(line in content for line in BLACKLIST):
                private_key_files.append(filename)

    if private_key_files:
        for private_key_file in private_key_files:
            result.message += f'Private key found: {private_key_file}\n'
        result.code |= Status.FAILURE
    return result
