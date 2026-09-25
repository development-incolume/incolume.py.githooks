"""Module Command Line Inteface."""

from __future__ import annotations

import argparse
import inspect
import logging
import platform
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import click
from icecream import ic

from incolume.py.githooks.commit_msg import get_msg
from incolume.py.githooks.core import (
    __package_name__,
    __version__,
    backup_file,
    debug_enable,
    get_git_diff,
    get_issue_from_branch,
)
from incolume.py.githooks.core.decorators import logging_call
from incolume.py.githooks.core.rules import (
    CONTEXT_SETTINGS_CLICK,
    RequestFl,
    Result,
    Status,
)
from incolume.py.githooks.core.utils import find_project_root
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
from incolume.py.githooks.validate_branchname import ValidateBranchname
from incolume.py.githooks.validate_filename import validate_filename

debug_enable()

if TYPE_CHECKING:
    from collections.abc import Sequence


logging.debug('Python %s', platform.python_version())
msg_commit_file: Path = find_project_root(__file__).joinpath(
    '.git', 'COMMIT_EDITMSG'
)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-len-first-line',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=True),
    help='Filenames to check',
)
@click.option(
    '--min-first-line',
    default=10,
    type=click.INT,
    required=False,
    help='Minimum Length of line for first line',
)
@click.option(
    '--max-first-line',
    default=50,
    type=click.INT,
    required=False,
    help='Maximum Length of line for first line',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@logging_call(logging.INFO, 'Checking length of first line in commit message.')
def check_len_first_line_commit_msg_cli(
    filenames: list[str],
    min_first_line: int = 10,
    max_first_line: int = 50,
    *,
    nonexequi: bool = False,
) -> int:
    """Check commit message."""
    results: list[Result] = []
    result_code: Status = Status.SUCCESS

    ic(
        f'{inspect.stack()[0][3]}: {sys.argv=}, '
        f'{filenames=}, {min_first_line=}, {max_first_line=}, {nonexequi=}'
    )
    logging.info(inspect.stack()[0][3])

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(result_code.value)

    for filename in filenames:
        ic(filename)
        results.extend((
            check_min_len_first_line_commit_msg(
                commit_msg_filepath=filename, len_line=min_first_line
            ),
            check_max_len_first_line_commit_msg(
                commit_msg_filepath=filename, len_line=max_first_line
            ),
        ))

    result_code = Status(
        not all(result.code == Status.SUCCESS for result in results)
    )

    for result in results:
        if result_code == Status.SUCCESS:
            click.secho(result.message, fg='green', file=sys.stdout)
        elif re.match(r'^(?:(?![OK]).)*$', result.message):
            click.secho(result.message, fg='red', err=True)
            ermsg = (
                'The first line of the commit violates'
                ' the defined minimum limits. (min: 10 and max: 50)'
            )
            raise click.ClickException(ermsg)

    return int(result_code.value)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-type-commit-msg',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'commit_msg_file',
    nargs=-1,
    type=click.Path(exists=True),
    default=(msg_commit_file,),
    required=False,
    help='Filename for commit message',
)
@logging_call(logging.INFO, 'Checking type of commit message.')
def check_type_commit_msg_cli(
    commit_msg_file: list[Path],
    *,
    nonexequi: bool = False,
) -> int:
    """Check commit message."""
    logging.info(inspect.stack()[0][3])

    result = check_type_commit_msg(*commit_msg_file)

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    click.secho(
        result.message, fg='green' if result.code == Status.SUCCESS else 'red'
    )
    return int(
        result.code.value
    )  # Validation passed or failure, allowing commit


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='is-valid-branchname',
)
@click.argument(
    'commit_msg_file',
    nargs=-1,
    type=click.Path(exists=True),
    required=False,
    help='Filename for commit message',
)
@click.argument(
    'commit_source', type=str, required=False, help='Commit source'
)
@click.argument('commit_hash', type=str, required=False, help='Commit hash')
@click.option(
    '--dev/--no-dev',
    default=False,
    help='(default: False) Consider `dev` as protected branch. ',
)
@click.option(
    '--tags/--no-tags',
    default=False,
    help='(default: False) Consider `tags` as protected branch. ',
)
@click.option(
    '--main/--no-main',
    default=True,
    help='(default: True) Consider `main` or `master` as protected branch. ',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@logging_call(logging.INFO, 'Checking valid branchname.')
def check_valid_branchname_cli(  # ruff: ignore[too-many-arguments]
    commit_msg_file: Path,
    commit_source: str,
    commit_hash: str,
    *,
    dev: bool = False,
    tags: bool = False,
    main: bool = True,
    nonexequi: bool = False,
) -> int:
    """Hookgit for check valid branchname.

    Hook designed for stages: pre-commit, pre-push, manual

    Returns:
        int: 0 to SUCCESS or 1 to FAILURE

    """
    logging.info(inspect.stack()[0][3])
    logging.debug(
        'commit_msg_file: %s, commit_source: %s, commit_hash: %s',
        commit_msg_file,
        commit_source,
        commit_hash,
    )
    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(Status.SUCCESS.value)

    result = ValidateBranchname().is_valid(
        protected_dev=dev,
        protected_tags=tags,
        protected_main=main,
    )

    if result.code == Status.SUCCESS:
        click.secho(result.message, fg='green')
    else:
        click.secho(result.message, fg='red', err=True)
        click.ClickException(result.message)

    return int(result.code.value)


@logging_call(logging.INFO, 'Checking valid filenames.')
def check_valid_filenames_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Maint entry point for the script.

    Hook designed for stages: pre-commit, pre-push, manual
    """
    codes: Status = Status.SUCCESS
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
    codes = Status.SUCCESS

    if args.nonexequi:
        return int(Status.SUCCESS.value)

    results: list[RequestFl] = [
        validate_filename(
            filename=filename, min_len=args.min_len, max_len=args.max_len
        )
        for filename in args.filenames
    ]
    for result in results:
        codes |= result.code
        for message in result.messages:
            click.secho(
                message, fg='green' if result.code == Status.SUCCESS else 'red'
            )

    return int(codes.value)


@logging_call(logging.INFO, 'Checking private keys in files.')
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
    result: Result = has_private_key(*args.filenames)
    click.secho(result.message, fg='red')
    return int(result.code.value)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='set-footer-signed-off-by',
)
@click.argument(
    'commit_msg_filename',
    type=Path,
    default=msg_commit_file,
    help='Arquivo de mensagem de commit',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@logging_call(
    logging.INFO, 'Processing footer signed-off-by in commit message.'
)
def footer_signedoffby_cli(
    commit_msg_filename: Path = msg_commit_file, *, nonexequi: bool = False
) -> int:
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
    logging.info(inspect.stack()[0][3])

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    commit_source = commit_msg_filename.read_text(encoding='utf-8')
    logging.info(commit_source)

    clean_commit_msg(commit_msg_filename)
    add_signed_off_by(commit_msg_filename)
    click.secho(
        'Added the "Signed-off-by" line into the commit message', fg='green'
    )
    add_blank_line_if_needed(commit_msg_filename)
    return int(Status.SUCCESS.value)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='effort-msg',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@logging_call(logging.INFO, 'Displaying effort message after commit.')
def effort_msg_cli(*, nonexequi: bool) -> int:
    """Run it.

    Hook designed for stages: post-commit, manual
    """
    logging.info(inspect.stack()[0][3])

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    click.secho(effort_msg(), fg='green')
    return 0


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='clean-commit-msg',
)
@click.argument(
    'commit_msg_file', required=True, help='Filename for commit message'
)
@click.argument('commit_source', required=False, help='Commit source')
@click.argument('commit_hash', required=False, help='Commit hash')
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@logging_call(logging.INFO, 'Cleaning commit message help text.')
def clean_commit_msg_cli(
    commit_msg_file: Path,
    commit_source: str,
    commit_hash: str,
    *,
    nonexequi: bool = False,
) -> int:
    """Remove the help message.

    Remove "# Please enter the commit message..." from help message.

    Hook designed for stages: pre-commit, pre-push, manual

    Args:
        commit_msg_file (Path or str): The path to the commit message file.

        commit_source (str): The source of the commit message.

        commit_hash (str): The commit hash.

        nonexequi (bool): if run hook.

    Returns:
        int: SUCCESS code if the operation completes.

    """
    logging.info(inspect.stack()[0][3])

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    ic(commit_msg_file, commit_source, commit_hash)

    commit_msg_file = Path(commit_msg_file)

    backup = backup_file(commit_msg_file, '.bak')
    logging.debug(backup)

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

    return int(Status.SUCCESS.value)


@logging_call(logging.INFO, 'Validating commit message format.')
def validate_format_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> Status:
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

    ic(fl := msg_commit_file)
    ic(fl.is_file())

    logging.debug('msgfile: %s', args)

    result = validate_format_commit_msg(*args.filenames)

    click.secho(
        result.message, fg='green' if result.code == Status.SUCCESS else 'red'
    )
    return result.code.value


@logging_call(logging.INFO, 'Checking pre-commit installation.')
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

    result = Status.SUCCESS
    files = list(Path.cwd().glob('.pre-commit-config.yaml'))
    ic(files)
    if not files:
        click.secho(
            '\n\n`pre-commit` configuration detected,'
            ' but `pre-commit install` was never ran.\n',
            fg='red',
        )
        result |= Status.FAILURE
    return int(result.value)


@logging_call(logging.INFO, 'Displaying commit message after commit.')
def get_msg_cli(argv: Sequence[str] | None = None) -> Status:
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
        click.secho(get_msg(fixed=args.fixed), fg='green')

    return Status.SUCCESS.value


@logging_call(logging.INFO, 'Inserting git diff into commit message.')
def insert_diff_cli(argv: Sequence[str] | None = None) -> Status:
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
        return Status.SUCCESS.value

    diff_output = get_git_diff()
    insert_git_diff(args.commit_msg_file, diff_output)

    return Status.SUCCESS.value


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=False)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='set-issue-from-branch',
)
@click.argument(
    'commit_msg_filepath',
    default=msg_commit_file.as_posix(),
    type=click.Path(exists=True),
    help='Caminho para o arquivo de mensagem de commit',
)
@click.argument(
    'commit_type',
    default='',
    required=False,
    type=str,
    help='---',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
def set_issue_from_branch_cli(
    commit_msg_filepath: str, commit_type: str, *, nonexequi: bool = False
) -> int:
    """CLI para extrair o número do ticket do nome do branch.

    Verifica se o hook foi chamado com a opção
    -m (mensagem fornecida pelo usuário)
    Se sim, evita sobrescrever a mensagem manualmente inserida
    """
    ic(f'{commit_msg_filepath=}, {commit_type=}, {nonexequi=}')
    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
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

    flin: Path = Path(commit_msg_filepath)
    issue_number = get_issue_from_branch()
    ic(f'{issue_number=}')

    if issue_number and flin.is_file():
        header = f'[ISSUE-{issue_number}] '

        with Path(commit_msg_filepath).open('r+', encoding='utf-8') as f:
            content = f.read()
            # Prependa o header se não existir já
            if not content.startswith(header):
                f.seek(0, 0)
                f.write(header + content)
                click.secho(
                    'Added ticket number '
                    f'{issue_number} to the commit message.',
                    fg='green',
                )
    return 0


if __name__ == '__main__':
    sys.exit(check_type_commit_msg_cli(sys.argv[1:]))
