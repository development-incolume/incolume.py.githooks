r"""Module for git hook.

#!/bin/sh

message='Boa! Continue trabalhando com dedicação!'
echo "\033[1;32m $message\033[0m\n";

"""
# ruff: noqa: T201

from colorama import Fore, Style


def effort_msg(message: str = '') -> None:
    """Effort message."""
    message = message or 'Boa! Continue trabalhando com dedicação!'
    print(f'{Fore.GREEN}{message}{Style.NORMAL}')
