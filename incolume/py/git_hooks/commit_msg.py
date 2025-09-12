"""Module to handle commit message hook."""

# ruff: noqa: T201

import random
import sys


def check():
    """Check arguments."""
    print('Number of arguments: %d' % len(sys.argv))
    print('Arguments List: %s' % str(sys.argv))


def get_msg(idx: int = 0, *, fixed: bool = False) -> None:
    """Get message."""
    msg = [
        'Boa! Continue o bom trabalho com a força, Jedi!',
        'Boa! Continue trabalhando campeão!',
        'Executado com sucesso.',
    ]
    base = '\n\033[92m{}\033[0m\n'
    if fixed:
        print(base.format(msg[idx]))
    else:
        print(base.format(msg[random.randint(0, len(msg) - 1)]))


def run():
    """Run it."""
    get_msg(0, True)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
