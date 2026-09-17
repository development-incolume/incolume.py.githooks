"""Module to validate commit messages."""

import argparse
import inspect
import pathlib
import sys
from collections.abc import Sequence

from click import secho
from icecream import ic

commit_types = [
    'chore',
    'docs',
    'feat',
    'fix',
    'refactor',
    'style',
    'test',
]


def run(argv: Sequence[str] | None = None) -> int:
    """Validate commit messages."""
    ic(f'{inspect.currentframe().f_code.co_name!s}: {sys.argv=}, {argv=}')  # type: ignore[union-attr]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'commit_msg_file',
        default='',
        help='Arquivo contendo a mensagem do commit',
    )
    args = parser.parse_args(argv)
    commit_msg_file = args.commit_msg_file

    commit_msg = (
        pathlib.Path(commit_msg_file).read_text(encoding='utf-8').strip()
    )

    if not any(commit_msg.startswith(msg) for msg in commit_types):
        secho(
            'Erros: As mensagens de commit devem ser de um dos tipos válidos: '
            f'({", ".join(commit_types)}).',
            fg='red',
        )
        return 1

    secho('Mensagem validada com sucesso.', fg='green')
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1:]))
