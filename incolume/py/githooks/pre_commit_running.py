"""Verify if pre-commit is installed."""

from __future__ import annotations

import sys
from pathlib import Path

import rich

from incolume.py.githooks import FAILURE, SUCCESS


def run() -> int:
    """Run it."""
    result = SUCCESS
    if not Path('.pre-commit-config.yaml').exists():
        rich.print(
            '[red]pre-commit configuration detected,'
            ' but `pre-commit install` was never run[/red]',
        )
        result |= FAILURE
    return sys.exit(result)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
