"""Verify if pre-commit is installed."""

# ruff: noqa: T201
from __future__ import annotations

import sys
from pathlib import Path

from colorama import Fore, Style

from incolume.py.githooks import FAILURE, SUCCESS


def run() -> int:
    """Run it."""
    result = SUCCESS
    if not Path('.pre-commit-config.yaml').exists():
        print(
            f'{Fore.RED}pre-commit configuration detected,'
            f' but `pre-commit install` was never run{Style.RESET_ALL}',
        )
        result |= FAILURE
    return sys.exit(result)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
