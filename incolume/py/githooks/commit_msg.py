"""Module to handle commit message hook."""

from __future__ import annotations

import secrets
import sys

import rich

from incolume.py.githooks.rules import MESSAGES


def check() -> None:
    """Check arguments."""
    rich.print(f'Number of arguments: {len(sys.argv)}')
    rich.print(f'Arguments List: {sys.argv!s}')


def get_msg(*, fixed: bool = False, messages: list[str] | None = None) -> str:
    """Get message."""
    messages = messages or MESSAGES
    msg = messages[0] if fixed else secrets.choice(messages)
    return f'\n[green]{msg}[/]\n'


def get_msg_cli() -> None:
    """Run it."""
    rich.print(get_msg())


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(get_msg_cli())
