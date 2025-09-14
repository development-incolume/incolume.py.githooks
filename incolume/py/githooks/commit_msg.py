"""Module to handle commit message hook."""

# ruff: noqa: T201
from colorama import Fore, Style
import secrets
import sys


def check() -> None:
    """Check arguments."""
    print(f'Number of arguments: {len(sys.argv)}')
    print(f'Arguments List: {sys.argv!s}')


def get_msg(*, fixed: bool = False) -> None:
    """Get message."""
    messages = [
        'Boa! Continue o bom trabalho com a força, Jedi!',
        'Boa! Continue trabalhando campeão!',
        'Executado com sucesso.',
    ]
    msg = messages[0] if fixed else secrets.choice(messages)
    result = f'\n{Fore.GREEN}' +f'{msg}'+f'{Style.RESSET_ALL}\n'

    print(result)


def run() -> None:
    """Run it."""
    get_msg()


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
