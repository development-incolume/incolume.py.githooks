"""Module Command Line Inteface."""

from __future__ import annotations

import argparse
import inspect
import logging
import platform
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import rich
from icecream import ic

from incolume.py.githooks.commit_msg import get_msg
from incolume.py.githooks.core import (
    Result,
    debug_enable,
    get_git_diff,
)
from incolume.py.githooks.detect_private_key import has_private_key
from incolume.py.githooks.effort_message import effort_msg
from incolume.py.githooks.footer_signedoffby import (
    add_blank_line_if_needed,
    add_signed_off_by,
    clean_commit_msg,
)
from incolume.py.githooks.gitdiff import insert_git_diff
from incolume.py.githooks.prepare_commit_msg import (
    check_max_len_first_line_commit_msg,
    check_min_len_first_line_commit_msg,
    check_type_commit_msg,
    validate_format_commit_msg,
)
from incolume.py.githooks.rules import (
    FAILURE,
    SUCCESS,
    Status,
)
from incolume.py.githooks.valid_filename import ValidateFilename
from incolume.py.githooks.validate_branchname import ValidateBranchname

debug_enable()

if TYPE_CHECKING:
    from collections.abc import Sequence


def check_len_first_line_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Check commit message."""
    results = []
    result_code: Status = Status.SUCCESS
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        'commit_source', default='', help='Origem do commit (ex.: template)'
    )
    parser.add_argument(
        'commit_hash', default='', help='Hash do commit ou vazio'
    )
    parser.add_argument(
        '--min-first-line',
        default=10,
        type=int,
        required=False,
        help='Minimum Length of line for first line',
    )
    parser.add_argument(
        '--max-first-line',
        default=50,
        type=int,
        required=False,
        help='Maximum Length of line for first line',
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )
    args = parser.parse_args(argv)

    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return result_code.value

    for filename in args.filenames:
        ic(filename)
        results.extend((
            check_min_len_first_line_commit_msg(
                commit_msg_filepath=filename, len_line=args.min_first_line
            ),
            check_max_len_first_line_commit_msg(
                commit_msg_filepath=filename, len_line=args.max_first_line
            ),
        ))
    for result in results:
        rich.print(result.message)
        result_code |= result.code

    return result_code.value  # Validation passed, allow commit


def check_type_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> sys.exit:
    """Check commit message."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )
    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    result = check_type_commit_msg(*args.filenames)

    if args.nonexequi:
        sys.exit(0)

    rich.print(result.message)
    sys.exit(result.code)  # Validation passed or failure, allowing commit


def check_valid_branchname_cli(argv: Sequence[str] | None = None) -> int:
    """Check valid branchname.

    Hook designed for stages: pre-commit, pre-push, manual

    Returns:
        int: 0 to SUCCESS or 1 to FAILURE

    """
    parser = argparse.ArgumentParser(
        description=('Hook Git em Python para validar branchname.')
    )
    parser.add_argument(
        'commit_msg_file',
        nargs='+',
        type=Path,
        help='Arquivo de mensagem de commit',
    )
    parser.add_argument(
        '--dev',
        default=False,
        dest='protected_dev',
        action='store_true',
        help='Consider dev as protected branch.',
    )
    parser.add_argument(
        '--tags',
        default=False,
        dest='protected_tags',
        action='store_true',
        help='Consider tags as protected branch.',
    )
    parser.add_argument(
        '--not-main',
        default=True,
        dest='protected_main',
        action='store_false',
        help='Desconsider main as protected branch.',
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Not run hook, ignore adding Signed-off-by',
    )

    args = parser.parse_args(argv)
    logging.debug(platform.python_version_tuple())
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return SUCCESS.value

    return ValidateBranchname().is_valid(
        protected_dev=args.protected_dev,
        protected_tags=args.protected_tags,
        protected_main=args.protected_main,
    )


def check_valid_filenames_cli(argv: Sequence[str] | None = None) -> int:
    """Maint entry point for the script.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    codes: Status = SUCCESS
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
        required=False,
        help='Minimum length for a filename.',
    )
    parser.add_argument(
        '--max-len',
        default=256,
        type=int,
        required=False,
        help='Maximum length for a filename.',
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )

    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return 0

    results: list[Result] = [
        ValidateFilename.is_valid(
            filename=filename, min_len=args.min_len, max_len=args.max_len
        )
        for filename in args.filenames
    ]
    for result in results:
        rich.print(result.message)
        codes |= result.code
    return codes.value


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
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )
    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return 0

    ic(args)
    result = has_private_key(*args.filenames)
    rich.print(result.message)
    return result.code.value


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
        'commit_msg_filename', type=Path, help='Arquivo de mensagem de commit'
    )
    parser.add_argument(
        'commit_source', default='', help='Origem do commit (pode ser vazio)'
    )
    parser.add_argument(
        'commit_hash', default='', help='Hash do commit (pode ser vazio)'
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Not run hook, ignore adding Signed-off-by',
    )

    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)
    commit_source = '' or args.commit_source

    ic(args)

    clean_commit_msg(args.commit_msg_filename)
    if not args.nonexequi:
        add_signed_off_by(args.commit_msg_filename)
    add_blank_line_if_needed(args.commit_msg_filename, commit_source)
    return SUCCESS.value


def effort_msg_cli(argv: Sequence[str] | None = None) -> int:
    """Run it.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    parser = argparse.ArgumentParser(
        description='Exibe mensagem de esforço após exito do commit.'
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )

    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return 0

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
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Do not run this hook.',
    )
    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return SUCCESS

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


def validate_format_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Run CLI for prepare-commit-msg hook.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Do not run this hook.',
    )
    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return 0

    ic(fl := Path('.git/COMMIT_EDITMSG'))
    ic(fl.is_file())

    logging.debug('msgfile: %s', args)

    result = validate_format_commit_msg(*args.filenames)

    rich.print(result.message)
    return result.code.value


def pre_commit_installed_cli(argv: Sequence[str] | None = None) -> int:
    """Run pre-commit-installed hook.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    parser = argparse.ArgumentParser(
        description='Validade pre-commit binary instalation.'
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )
    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)

    if args.nonexequi:
        return 0

    result = SUCCESS
    files = list(Path.cwd().glob('.pre-commit-config.yaml'))
    ic(files)
    if not files:
        rich.print(
            '\n\n[red]`pre-commit` configuration detected,'
            ' but `pre-commit install` was never ran.[/red]\n',
        )
        result |= FAILURE
    return result.value


def get_msg_cli(argv: Sequence[str] | None = None) -> int:
    """Run it."""
    parser = argparse.ArgumentParser(
        description='Exibe mensagens de sucesso após exito do commit.'
    )
    parser.add_argument(
        '--fixed',
        default=False,
        dest='fixed',
        action='store_true',
        help='Fixar messagem de hook.',
    )
    parser.add_argument(
        '--nonexequi',
        default=False,
        dest='nonexequi',
        action='store_true',
        help='Não executar hook.',
    )

    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)
    ic(args)

    if not args.nonexequi:
        rich.print(get_msg(fixed=args.fixed))

    return SUCCESS.value


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
        'commit_hash', default='', help='Hash do commit ou vazio'
    )
    parser.add_argument(
        '--nonexequi',
        dest='nonexequi',
        action='store_false',
        help='Não executar hook.',
    )

    args = parser.parse_args(argv)
    logging.info(inspect.stack()[0][3])
    logging.debug('msgfile: %s', args)
    ic(args)

    if not args.nonexequi:
        return SUCCESS.value

    diff_output = get_git_diff()
    insert_git_diff(args.commit_msg_file, diff_output)

    return SUCCESS.value
