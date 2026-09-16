"""Module to validate commit messages."""

import inspect
import pathlib
import sys

import click
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


@click.command()
@click.argument(
    'commit_msg_file',
    default='',
    type=click.Path(exists=True),
    help='Arquivo contendo a mensagem do commit',
)
def run(commit_msg_file: str) -> int:
    """Validate commit messages."""
    ic(f'{inspect.currentframe().f_code.co_name!s}: {sys.argv=}')  # type: ignore[union-attr]

    commit_msg = (
        pathlib.Path(commit_msg_file).read_text(encoding='utf-8').strip()
    )

    if not any(commit_msg.startswith(msg) for msg in commit_types):
        click.secho(
            'Erros: As mensagens de commit devem ser de um dos tipos válidos: '
            f'({", ".join(commit_types)}).',
            fg='red',
        )
        return 1

    click.secho('Mensagem validada com sucesso.', fg='green')
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1:]))
