"""Module to handle commit message hook."""

# ruff: noqa: T201

import secrets
import sys


def check() -> None:
    """Check arguments."""
    print(f'Number of arguments: {len(sys.argv)}')
    print(f'Arguments List: {sys.argv!s}')


def get_msg(*, fixed: bool = False) -> None:
    """Get message."""
    msg = [
        'Boa! Continue o bom trabalho com a força, Jedi!',
        'Boa! Continue trabalhando campeão!',
        'Executado com sucesso.',
    ]
    base = '\n\033[92m{}\033[0m\n'
    result = base.format(msg[0]) if fixed else base.format(secrets.choice(msg))
    print(result)


def run() -> None:
    """Run it."""
    get_msg(0, fixed=True)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
