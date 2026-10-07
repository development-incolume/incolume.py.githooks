"""Module to handle effort commit message hook."""

import secrets

from colorama import Fore, Style

from incolume.py.githooks.core.rules import MESSAGES


def effort_msg(message: str = '') -> str:
    """Effort message."""
    message = message or 'Great. Keep up the hard work!!'
    return f'{Fore.GREEN}{message}{Style.NORMAL}'


def effort_random_msg(
    *, fixed: bool = False, messages: list[str] | None = None
) -> str:
    """Get message."""
    messages = messages or MESSAGES
    msg = messages[0] if fixed else secrets.choice(messages)
    return f'\n{msg}\n'
