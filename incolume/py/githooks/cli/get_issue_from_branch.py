"""Module."""

# !/usr/bin/env python
import sys

import click
from icecream import ic


@click.command()
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
    helf='---',
)
@click.option(
    '--nonexequi',
    default=False,
    help='Não executar hook.',
)
def main(*args: str, **kwargs: dict[str, str]) -> int:
    """Extrair o número do ticket do branchname e adicioná-lo à commit-msg.

    Verifica se o hook foi chamado
    com a opção -m (mensagem fornecida pelo usuário)
    Se sim, evita sobrescrever a mensagem manualmente inserida
    """
    ic(f'{sys.argv=}, {args=}, {kwargs=}')

    # if 'nonexequi' in argv or commit_type == 'message':
    #     return

    # try:
    #     commit_msg_filepath = sys.argv[1]
    # except IndexError:
    #     commit_msg_filepath = '.git/COMMIT_EDITMSG'
    # ic(f'{commit_msg_filepath=}')
    # flin: pathlib.Path = pathlib.Path(commit_msg_filepath)
    # issue_number = get_issue_from_branch()
    # ic(f'{issue_number=}')

    # if issue_number and flin.is_file():
    #     header = f'[ISSUE-{issue_number}] '

    #     with flin.open('r+', encoding='utf-8') as f:
    #         content = f.read()
    #         # Prependa o header se não existir já
    #         if not content.startswith(header):
    #             f.seek(0, 0)
    #             f.write(header + content)


if __name__ == '__main__':
    main()
    sys.exit(main(sys.argv[1:]))
