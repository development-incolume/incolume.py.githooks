"""Module."""

# !/usr/bin/env python
import pathlib
import sys
from collections.abc import Sequence

from icecream import ic

from incolume.py.githooks.core import get_issue_from_branch


def main(argv: Sequence[str] | None = None) -> None:
    """Extrair o número do ticket do branchname e adicioná-lo à commit-msg.

    Verifica se o hook foi chamado
    com a opção -m (mensagem fornecida pelo usuário)
    Se sim, evita sobrescrever a mensagem manualmente inserida
    """
    ic(f'{sys.argv=}, {argv=}')
    argv = sys.argv or argv or []

    try:
        commit_type = argv[2]
    except IndexError:
        commit_type = ''
    ic(f'{commit_type=}')

    if commit_type == 'message':
        return

    try:
        commit_msg_filepath = sys.argv[1]
    except IndexError:
        commit_msg_filepath = '.git/COMMIT_EDITMSG'
    ic(f'{commit_msg_filepath=}')
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


if __name__ == '__main__':
    main()
