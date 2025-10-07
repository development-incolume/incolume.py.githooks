"""Module Command Line Inteface."""

from __future__ import annotations

import argparse
import logging
import platform
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import rich
from colorama import Fore, Style
from icecream import ic

from incolume.py.githooks.commit_msg import get_msg
from incolume.py.githooks.detect_private_key import has_private_key
from incolume.py.githooks.effort_message import effort_msg
from incolume.py.githooks.footer_signedoffby import (
    add_blank_line_if_needed,
    add_signed_off_by,
    clean_commit_msg,
)
from incolume.py.githooks.gitdiff import get_git_diff, insert_git_diff
from incolume.py.githooks.prepare_commit_msg import (
    check_max_len_first_line_commit_msg,
    check_min_len_first_line_commit_msg,
    check_type_commit_msg,
    prepare_commit_msg,
)
from incolume.py.githooks.rules import FAILURE, RULE_BRANCHNAME, SUCCESS
from incolume.py.githooks.utils import Result, debug_enable, get_branchname
from incolume.py.githooks.valid_filename import ValidateFilename

debug_enable()

if TYPE_CHECKING:
    from collections.abc import Sequence


def check_len_first_line_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Check commit message."""
    results = []
    result_code = SUCCESS
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        '--min-first-line',
        default=10,
        type=int,
        help='Minimum Length of line for first line',
    )
    parser.add_argument(
        '--max-first-line',
        default=50,
        type=int,
        help='Maximum Length of line for first line',
    )
    args = parser.parse_args(argv)
    for filename in args.filenames:
        ic(filename)
        results.extend((
            check_min_len_first_line_commit_msg(
                filename, len_line=args.min_first_line
            ),
            check_max_len_first_line_commit_msg(
                filename, len_line=args.max_first_line
            ),
        ))
    for result in results:
        rich.print(result.message)
        result_code |= result.code

    sys.exit(result_code)  # Validation passed, allow commit


def check_type_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> sys.exit:
    """Check commit message."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    result = check_type_commit_msg(*args.filenames)
    rich.print(result.message)
    sys.exit(result.code)  # Validation passed or failure, allowing commit


def check_valid_branchname() -> int:
    """Check valid branchname.

    Hook designed for stages: pre-commit, pre-push, manual

    Returns:
        int: SUCCESS or FAILURE

    """
    logging.debug(platform.python_version_tuple())
    result = f'{Fore.GREEN}Branching name rules. [OK]{Style.RESET_ALL}'
    status = SUCCESS
    if not re.match(RULE_BRANCHNAME, get_branchname()):
        result = (
            f'{Fore.RED}Your commit was rejected due to branching name '
            'incompatible with rules.\n'
            "Please rename your branch with '<(enhancement|feature|feat"
            f"|bug|bugfix|fix)>/epoch#<timestamp>' syntax{Style.RESET_ALL}"
        )
        status |= FAILURE
    rich.print(result)
    return status


def check_valid_filenames_cli(argv: Sequence[str] | None = None) -> int:
    """Maint entry point for the script.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    codes: int = SUCCESS
    parser = argparse.ArgumentParser(
        prog='validate-filename',
    )
    parser.add_argument(
        'filenames',
        nargs='+',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--min-len',
        default=3,
        type=int,
        help='Minimum length for a filename.',
    )
    parser.add_argument(
        '--max-len',
        default=256,
        type=int,
        help='Maximum length for a filename.',
    )

    args = parser.parse_args(argv)

    results: list[Result] = [
        ValidateFilename.is_valid(
            filename=filename, min_len=args.min_len, max_len=args.max_len
        )
        for filename in args.filenames
    ]
    for result in results:
        rich.print(result.message)
        codes |= result.code
    return codes


def detect_private_key_cli(argv: Sequence[str] | None = None) -> int:
    """CLI to check private key.

    Hook designed for stages: all

    Args:
        argv (Sequence[str] | None, optional): _description_. Defaults to None.

    Returns:
        int: _description_

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    ic(args)
    result = has_private_key(*args.filenames)
    rich.print(result.message)
    return result.code


def footer_signedoffby_cli(argv: Sequence[str] | None = None) -> int:
    """Função principal que processa os argumentos.

    E aplica as transformações no arquivo de commit.

    Hook designed for stages: pre-commit, pre-push, manual

    Fluxo:
    1. Remove linhas desnecessárias do template de commit.
    2. Adiciona 'Signed-off-by' do committer atual.
    3. Adiciona linha em branco no topo se necessário.

    Returns:
        None

    """
    parser = argparse.ArgumentParser(
        description=(
            'Hook Git em Python equivalente ao script original em Perl/Shell.'
        )
    )
    parser.add_argument(
        'commit_msg_file', type=Path, help='Arquivo de mensagem de commit'
    )
    parser.add_argument(
        'commit_source', default='', help='Origem do commit (pode ser vazio)'
    )
    parser.add_argument(
        'commit_hash', default='', help='SHA1 do commit (pode ser vazio)'
    )
    parser.add_argument(
        '--signoff',
        default=True,
        dest='signed',
        action='store_false',
        help='Não adicionar Signed-off-by',
    )

    args = parser.parse_args(argv)

    clean_commit_msg(args.commit_msg_file)
    if args.signed:
        add_signed_off_by(args.commit_msg_file)
    add_blank_line_if_needed(args.commit_msg_file, args.commit_source)
    return SUCCESS


def effort_msg_cli() -> int:
    """Run it.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    rich.print(effort_msg())
    return 0


def clean_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Remove the help message.

    Remove "# Please enter the commit message..." from help message.

    Hook designed for stages: pre-commit, pre-push, manual

    Args:
        argv: Arguments values sequence:
          - commit_msg_file (Path or str): The path to the commit message file.
          - commit_source (str): The source of the commit message.
          - commit_hash (str): The commit hash.

    Returns:
        int: SUCCESS code if the operation completes.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('commit_msg_file', help='Filename for commit message')
    parser.add_argument('commit_source', help='Commit source')
    parser.add_argument('commit_hash', help='Commit hash')
    args = parser.parse_args(argv)
    commit_msg_file = args.commit_msg_file
    commit_source = args.commit_source
    commit_hash = args.commit_hash

    ic(commit_msg_file, commit_source, commit_hash)

    commit_msg_file = Path(commit_msg_file)

    backup = commit_msg_file.with_suffix(commit_msg_file.suffix + '.bak')
    backup.write_bytes(commit_msg_file.read_bytes())

    result = []
    skipping = False

    for line in commit_msg_file.read_text(encoding='utf-8').splitlines(
        keepends=True
    ):
        if not skipping and line.lstrip().startswith(
            'Please enter the commit message'
        ):
            skipping = True
            continue
        if skipping and line.strip() == '#':
            skipping = False
            continue
        if not skipping:
            result.append(line)

    commit_msg_file.write_text(''.join(result), encoding='utf-8')

    return SUCCESS


def prepare_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> sys.exit:
    """Run CLI for prepare-commit-msg hook.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    ic(fl := Path('.git/COMMIT_EDITMSG'))
    ic(fl.is_file())
    logging.debug('msgfile: %s', args)

    result = prepare_commit_msg(*args.filenames)

    rich.print(result.message)
    sys.exit(result.code)


def pre_commit_installed_cli() -> int:
    """Run pre-commit-installed hook.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    result = SUCCESS
    files = list(Path.cwd().glob('.pre-commit-config.yaml'))
    ic(files)
    if not files:
        rich.print(
            '\n\n[red]`pre-commit` configuration detected,'
            ' but `pre-commit install` was never ran.[/red]\n',
        )
        result |= FAILURE
    return result


def get_msg_cli() -> None:
    """Run it."""
    rich.print(get_msg())


def insert_diff_cli(argv: Sequence[str] | None = None) -> int:
    """CLI for module gitdiff."""
    parser = argparse.ArgumentParser(
        description='Processa mensagens de commit'
        ' como no hook original em Perl.'
    )
    parser.add_argument(
        'commit_msg_file', type=Path, help='Arquivo da mensagem de commit'
    )
    parser.add_argument(
        'commit_source', default='', help='Origem do commit (ex.: template)'
    )
    parser.add_argument(
        'commit_hash', default='', help='SHA1 do commit ou vazio'
    )

    args = parser.parse_args(argv)
    ic(args)

    diff_output = get_git_diff()
    insert_git_diff(args.commit_msg_file, diff_output)

    return SUCCESS
