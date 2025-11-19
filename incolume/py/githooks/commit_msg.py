"""Module to handle commit message hook."""

from __future__ import annotations

import secrets

from incolume.py.githooks.rules import MESSAGES


def get_msg(*, fixed: bool = False, messages: list[str] | None = None) -> str:
    """Get message."""
    messages = messages or MESSAGES
    msg = messages[0] if fixed else secrets.choice(messages)
    return f'\n[green]{msg}[/green]\n'
