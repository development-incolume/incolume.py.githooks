r"""Module for git hook.

#!/bin/sh

message='Boa! Continue trabalhando com dedicação!'
echo "\033[1;32m $message\033[0m\n";

"""
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
