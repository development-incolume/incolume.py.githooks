"""Module."""

import pathlib
import sys

import click
from icecream import ic

from incolume.py.githooks.core import (
    CONTEXT_SETTINGS_CLICK,
    debug_enable,
    get_issue_from_branch,
)

debug_enable()


@click.command(context_settings=CONTEXT_SETTINGS_CLICK)
@click.argument(
    'commit_msg_filepath',
    default='.git/COMMIT_EDITMSG',
    type=click.Path(exists=True),
    help='Caminho para o arquivo de mensagem de commit',
)
@click.argument(
    'commit_type',
    default='',
    type=str,
    help='---',
)
@click.option(
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Não executar este hook.',
)
def main(
    commit_msg_filepath: str = '.git/COMMIT_EDITMSG',
    commit_type: str = '',
    *,
    nonexequi: bool = False,
) -> int:
    """Extrair o número do ticket do branchname e adicioná-lo à commit-msg."""
    ic(f'{commit_msg_filepath=}, {commit_type=}, {nonexequi=}')
    if nonexequi:
        click.secho(
            'Hook não executado devido à opção `--nonexequi`.',
            fg='yellow',
        )
        return 0

    # Verifica se o hook foi chamado
    # com a opção -m (mensagem fornecida pelo usuário)
    # Se sim, evita sobrescrever a mensagem manualmente inserida
    if commit_type == 'message':
        click.secho(
            'Hook não executado devido ao commit_type=message.',
            fg='yellow',
        )
        return 0

    flin: pathlib.Path = pathlib.Path(commit_msg_filepath)
    issue_number = get_issue_from_branch()
    ic(f'{issue_number=}')

    if issue_number and flin.is_file():
        header = f'[ISSUE-{issue_number}] '

        with flin.open('r+', encoding='utf-8') as f:
            content = f.read()
            # Prependa o header se não existir já
            if not content.startswith(header):
                f.seek(0, 0)
                f.write(header + content)
                click.secho(
                    f'Adicionado o número do ticket {issue_number}'
                    ' à mensagem de commit.',
                    fg='green',
                )
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
