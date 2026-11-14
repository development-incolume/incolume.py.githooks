"""Module Command Line Inteface."""

from __future__ import annotations

import inspect
import logging
import os
import platform
import re
import sys
from pathlib import Path
from typing import Any

import click
from icecream import ic

from incolume.py.githooks.check_commit_footer import check_commit_footer
from incolume.py.githooks.check_manual_changelog import check_manual_changelog
from incolume.py.githooks.check_manual_version import check_manual_version
from incolume.py.githooks.check_type_from_status import (
    check_type_from_status,
)
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
from incolume.py.githooks.core.utils import (
    find_project_root,
    get_commit_msg_file,
    get_hooks_dir,
    interpreter_missing,
)
from incolume.py.githooks.detect_private_key import has_private_key
from incolume.py.githooks.effort_message import effort_msg, effort_random_msg
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
from incolume.py.githooks.type_from_status import set_type_commit_msg
from incolume.py.githooks.validate_branchname import ValidateBranchname
from incolume.py.githooks.validate_filename import validate_filename

logging.warning('Python %s', platform.python_version())


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-len-first-line',
)
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
@click.pass_context
@logging_call(logging.INFO, 'Checking length of first line in commit message.')
def check_len_first_line_commit_msg_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check length of first line in commit message.

    Args:
      kwargs:
        filenames: list[str],
        min_first_line: int = 10,
        max_first_line: int = 50,
        nonexequi: bool = False,
      ctx: contexto CLI

    Examples:
        check-len-first-line .git/COMMIT_EDITMSG
        check-len-first-line --max-first-line 50 .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = ctx.params.get('filenames') or []
    min_first_line = ctx.params.get('min_first_line') or 10
    max_first_line = ctx.params.get('max_first_line') or 50
    nonexequi = ctx.params.get('nonexequi')
    results: list[Result] = []
    result_code: Status = Status.SUCCESS

    ic(
        f'{inspect.stack()[0][3]}: {sys.argv=}, '
        f'{filenames=}, {min_first_line=}, {max_first_line=}, {nonexequi=}'
    )
    logging.warning(inspect.stack()[0][3])

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


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-type-commit-msg',
)
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
    required=False,
    help='Filename for commit message',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking type of commit message.')
def check_type_commit_msg_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check type of commit message.

    Args:
      kwargs:
        commit_msg_file: list[Path],
        nonexequi: bool = False,
      ctx: context CLI

    Examples:
        check-type-commit-msg .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    commit_msg_file = ctx.params.get('commit_msg_file') or [
        get_commit_msg_file()
    ]
    nonexequi = ctx.params.get('nonexequi')

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


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='is-valid-branchname',
)
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
@click.pass_context
@logging_call(logging.INFO, 'Checking valid branchname.')
def check_valid_branchname_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> click.Context:
    """Check if the branch name is valid.

    Hook designed for stages: pre-commit, pre-push, manual
    Args:
      kwargs:
        commit_msg_file: Path,
        commit_source: str,
        commit_hash: str,
        dev: bool = False,
        tags: bool = False,
        main: bool = True,
        nonexequi: bool = False,

    Returns:
        int: 0 to SUCCESS or 1 to FAILURE

    Examples:
        is-valid-branchname
        is-valid-branchname --dev

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    commit_msg_file = ctx.params.get('commit_msg_file ')
    commit_source = ctx.params.get('commit_source ')
    commit_hash = ctx.params.get('commit_hash ')
    dev = ctx.params.get('dev')
    tags = ctx.params.get('tags')
    main = ctx.params.get('main')
    nonexequi = ctx.params.get('nonexequi')

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
        ctx.exit(Status.SUCCESS.value)

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

    ctx.exit(result.code.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='is-valid-filename',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='is-valid-filename',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.option(
    '--min-len',
    default=3,
    type=click.INT,
    required=False,
    help='Minimum Length of line for filename',
)
@click.option(
    '--max-len',
    default=256,
    type=click.INT,
    required=False,
    help='Maximum Length of line for filename',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking valid filenames.')
def check_valid_filenames_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Validate filenames to process.

    Hook designed for stages: pre-commit, pre-push, manual

    Examples:
        is-valid-filename incolume/py/githooks/cli/cli.py
        is-valid-filename --max-len 256 incolume/py/githooks/cli/cli.py

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    codes: Status = Status.SUCCESS
    filenames = ctx.params.get('filenames')
    nonexequi = ctx.params.get('nonexequi')
    min_len = ctx.params.get('min_len')
    max_len = ctx.params.get('max_len')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        ctx.exit(Status.SUCCESS.value)

    results: list[RequestFl] = [
        validate_filename(filename=filename, min_len=min_len, max_len=max_len)
        for filename in filenames  # type: ignore[union-attr]
    ]
    for result in results:
        codes |= result.code
        for message in result.messages:
            click.secho(
                message,
                fg='green' if result.code == Status.SUCCESS else 'red',
                err=True,
            )
    ic(ctx)
    ctx.exit(codes.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='detect-key',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='detect-key',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking private keys in files.')
def detect_private_key_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """CLI to check private key.

    Hook designed for stages: all

    Examples:
        detect-key incolume/py/githooks/cli/cli.py

    """
    ic(f'{kwargs}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = [Path(fl) for fl in ctx.params.get('filenames')]  # type: ignore[union-attr]
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return ctx.exit(0)

    result: Result = has_private_key(*filenames)
    click.secho(result.message, fg='red')
    return ctx.exit(result.code.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='set-footer-signed-off-by',
)
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
    default=None,
    help='Arquivo de mensagem de commit',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(
    logging.INFO, 'Processing footer signed-off-by in commit message.'
)
def footer_signedoffby_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Process footer signed-off-by in commit message.

    Aplly changes into commit file.

    Hook designed for stages: pre-commit, pre-push, manual

    Flow:

      1. Removes unnecessary lines from the commit template;

      2. Adds `Signed-off-by` from the current committer


      3. Add a blank line at the top if necessary.

    Returns:
        None

    Examples:
        set-footer-signed-off-by .git/COMMIT_EDITMSG

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    commit_msg_filename: Path = (
        ctx.params.get('commit_msg_filename') or get_commit_msg_file()
    )
    nonexequi: bool = ctx.params.get('nonexequi', False)

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    commit_source = commit_msg_filename.read_text(encoding='utf-8')
    logging.warning(commit_source)

    clean_commit_msg(commit_msg_filename)
    add_signed_off_by(commit_msg_filename)
    click.secho(
        'Added the "Signed-off-by" line into the commit message', fg='green'
    )
    add_blank_line_if_needed(commit_msg_filename)
    return int(Status.SUCCESS.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='effort-msg',
)
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
@click.pass_context
@logging_call(logging.INFO, 'Displaying effort message after commit.')
def effort_msg_cli(ctx: click.Context, **kwargs: dict[str, Any]) -> int:
    """Display success messages after a successful commit.

    Hook designed for stages: post-commit, manual

    Examples:
        effort-msg

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    if ctx.params.get('nonexequi'):
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    click.secho(effort_msg(), fg='green')
    return 0


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=True,
    name='clean-commit-msg',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='clean-commit-msg',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'commit_msg_file', required=True, help='Filename for commit message'
)
@click.argument('commit_source', required=False, help='Commit source')
@click.argument('commit_hash', required=False, help='Commit hash')
@click.pass_context
@logging_call(logging.INFO, 'Cleaning commit message help text.')
def clean_commit_msg_cli(ctx: click.Context, **kwargs: dict[str, Any]) -> int:
    """Remove the help message.

    Remove "# Please enter the commit message..." from help message.

    Hook designed for stages: pre-commit, pre-push, manual

    Args:
        ctx: context
        kwargs: click params, including ``commit_msg_file`` (path to the
            commit message file), ``commit_source``, ``commit_hash`` and
            ``nonexequi``.

    Returns:
        int: SUCCESS code if the operation completes.

    Examples:
        clean-commit-msg .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    commit_msg_file = (
        ctx.params.get('commit_msg_file') or get_commit_msg_file()
    )
    commit_source = ctx.params.get('commit_source')
    commit_hash = ctx.params.get('commit_hash')
    nonexequi = ctx.params.get('nonexequi')

    ic(commit_msg_file, commit_source, commit_hash)
    commit_msg_file = Path(commit_msg_file)

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    backup = backup_file(commit_msg_file)
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


@click.command(
    name='is-valid-msg-commit',
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='is-valid-msg-commit',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    required=False,
    help='Filenames for commit messages',
)
@click.pass_context
@logging_call(logging.INFO, 'Validating commit message format.')
def validate_format_commit_msg_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Validate commit message.

    Hook designed for stages: commit-msg, manual

    Examples:
        is-valid-msg-commit .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    nonexequi = ctx.params.get('nonexequi')
    filenames = ctx.params.get('filenames') or None

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        ctx.exit(0)

    result: Result = validate_format_commit_msg(filenames=filenames)

    click.secho(
        result.message, fg='green' if result.code == Status.SUCCESS else 'red'
    )
    ctx.exit(result.code.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='is-precommit-installed',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='is-precommit-installed',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking pre-commit installation.')
def pre_commit_installed_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Validate the pre-commit binary installation.

    Hook designed for stages: pre-commit, pre-push, manual

    Examples:
        is-precommit-installed

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    if ctx.params.get('nonexequi'):
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        ctx.exit(0)

    result = Status.SUCCESS
    files = list(find_project_root().glob('.pre-commit-config.yaml'))
    ic(files)
    if not files:
        result |= Status.FAILURE
        click.secho(
            '\n\nConfiguration file ".pre-commit-config.yaml" not detected',
            fg='red',
        )
    else:
        hooks_dir = get_hooks_dir()
        bins = tuple(
            hooks_dir / x
            for x in (
                'pre-commit',
                'pre-push',
                'prepare-commit-msg',
                'commit-msg',
                'post-commit',
            )
        )
        if not all(os.access(x, os.X_OK) for x in bins):
            result |= Status.FAILURE
            click.secho(
                '\n\n`pre-commit` configuration detected,'
                ' but `pre-commit install` was never ran.\n',
                fg='red',
            )
        else:
            broken = [x for x in bins if interpreter_missing(x)]
            if broken:
                result |= Status.FAILURE
                click.secho(
                    '\n\n`pre-commit` hooks instalados, mas com '
                    'interpretador inexistente: '
                    f'{", ".join(x.name for x in broken)}.\n',
                    fg='red',
                )
    ctx.exit(result.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='effort-random-msg',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='effort-random-msg',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.option(
    '--fixed',
    '-F',
    default=False,
    is_flag=True,
    help='Pin a hook message.',
)
@click.pass_context
@logging_call(logging.INFO, 'Displaying commit message after commit.')
def effort_random_msg_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Display a random success message after a successful commit.

    Hook designed for stages: post-commit, manual

    Args:
      kwargs:
        fixed: bool = False,
        nonexequi: bool = False
      ctx: context CLI

    Examples:
        effort-random-msg
        effort-random-msg --fixed

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    fixed = ctx.params.get('fixed')
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    click.secho(effort_random_msg(fixed=fixed), fg='green')

    return 0


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=True,
    name='insert-diff-commit',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='insert-diff-commit',
)
@click.option(
    '--nonexequi',
    '-N',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.argument(
    'commit_msg_file',
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False),
    required=False,
    help='Filename for commit message',
)
@click.argument(
    'commit_source', default='', required=False, help='Commit source'
)
@click.argument('commit_hash', default='', required=False, help='Commit hash')
@click.pass_context
@logging_call(logging.INFO, 'Inserting git diff into commit message.')
def insert_diff_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Process commit messages adding git-diff.

    Examples:
        insert-diff-commit .git/COMMIT_EDITMSG

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    commit_msg_file = ctx.params.get('commit_msg_file')
    commit_source = ctx.params.get('commit_source', '')
    commit_hash = ctx.params.get('commit_hash', '')
    nonexequi = ctx.params.get('nonexequi', False)

    if not commit_msg_file:
        commit_msg_file = get_commit_msg_file()

    match commit_msg_file:
        case list() | tuple() | set():
            fl = Path(next(iter(commit_msg_file)))
        case str():
            fl = Path(commit_msg_file)
        case Path():
            fl = commit_msg_file
        case None:
            fl = get_commit_msg_file()

    logging.debug(
        'commit_msg_file=%s commit_source=%s commit_hash=%s',
        commit_msg_file,
        commit_source,
        commit_hash,
    )

    if nonexequi or ctx.params.get('nonexequi'):
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        ctx.exit(Status.SUCCESS.value)

    diff_output = get_git_diff()
    ic(f'{fl=}')
    ic(f'{diff_output=}')
    logging.debug('fl="%s", diff_output="%s"', fl, diff_output)
    insert_git_diff(fl, diff_output)

    ctx.exit(Status.SUCCESS.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='set-issue-from-branch',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='set-issue-from-branch',
)
@click.argument(
    'commit_msg_filepath',
    type=click.Path(exists=True),
    help='Fullpath to the commit message file',
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
@click.pass_context
def set_issue_from_branch_cli(
    ctx: click.Context,
    /,
    **kwargs: dict[str, Any],
) -> int:
    """CLI to extract the ticket number from the branch name.

    Checks whether the hook was called with the
    -m option (user-provided message)
    If so, it prevents the manually entered message from being overwritten

    Examples:
        set-issue-from-branch .git/COMMIT_EDITMSG

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    commit_msg_filepath = (
        ctx.params.get('commit_msg_filepath') or get_commit_msg_file()
    )
    commit_type = ctx.params.get('commit_type')
    nonexequi = ctx.params.get('nonexequi')

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
            'Hook not executed because of commit_type=message.',
            fg='yellow',
        )
        return 0

    flin = Path(commit_msg_filepath)
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


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='set-type-from-status',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='set-type-from-status',
)
@click.argument(
    'commit_msg_filepath',
    type=click.Path(exists=True),
    help='Fullpath to the commit message file',
)
@click.argument(
    'commit_type',
    default='',
    required=False,
    type=str,
    help='Commit source informed by git',
)
@click.argument(
    'commit_hash',
    default='',
    required=False,
    type=str,
    help='Commit hash informed by git',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
def set_type_from_status_cli(
    ctx: click.Context,
    /,
    **kwargs: dict[str, Any],
) -> int:
    """Inject the Conventional Commits type deduced from staged files.

    An existing type in the message is never overwritten.

    Args:
        ctx: click context.
        kwargs: additional keyword arguments passed by the hook.

    Returns:
        0 if the type was injected successfully; 1 otherwise.

    Examples:
        set-type-from-status .git/COMMIT_EDITMSG

    """
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)

    commit_msg_filepath = ctx.params.get('commit_msg_filepath')
    commit_type = ctx.params.get('commit_type') or os.environ.get(
        'PRE_COMMIT_COMMIT_MSG_SOURCE', ''
    )
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return 0

    result: Result = set_type_commit_msg(
        commit_msg_filepath,
        commit_type=commit_type,
    )
    click.secho(
        result.message,
        fg='green' if result.code == Status.SUCCESS else 'red',
        err=result.code != Status.SUCCESS,
    )
    return int(result.code.value)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-commit-footer',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-commit-footer',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking footers in commit message.')
def check_commit_footer_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check footers of commit message.

    Args:
      kwargs:
        filenames: list[str],
        nonexequi: bool = False,
      ctx: contexto CLI

    Examples:
        check-commit-footer .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = ctx.params.get('filenames') or []
    nonexequi = ctx.params.get('nonexequi')

    ic(f'{inspect.stack()[0][3]}: {sys.argv=}, {filenames=}, {nonexequi=}')
    logging.warning(inspect.stack()[0][3])

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(Status.SUCCESS.value)

    result_code = check_commit_footer(list(filenames))

    if result_code == int(Status.SUCCESS.value):
        click.secho('Commit footers are valid.', fg='green', file=sys.stdout)
    else:
        ermsg = 'The commit message contains invalid footers.'
        raise click.ClickException(ermsg)

    return int(result_code)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-manual-version',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-manual-version',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking manual version in commit message.')
def check_manual_version_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check a manual version change against the commit message.

    Args:
        ctx: click context.
        kwargs: additional keyword arguments. Expected keys: filenames,
            nonexequi.

    Returns:
        0 if the manual version check passed; 1 otherwise.

    Examples:
        check-manual-version .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = ctx.params.get('filenames') or []
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(Status.SUCCESS.value)

    result_code = check_manual_version(list(filenames))

    if result_code == int(Status.SUCCESS.value):
        click.secho('Manual version check passed.', fg='green')
    else:
        ermsg = 'The version changed without a "build:" commit message.'
        raise click.ClickException(ermsg)

    return int(result_code)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-manual-changelog',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-manual-changelog',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking manual changelog in commit message.')
def check_manual_changelog_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check a manual changelog change against the commit message.

    Args:
        ctx: click context.
        kwargs: additional keyword arguments. Expected keys: filenames,
            nonexequi.

    Returns:
        0 if the manual changelog check passed; 1 otherwise.

    Examples:
        check-manual-changelog .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = ctx.params.get('filenames') or []
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(Status.SUCCESS.value)

    result_code = check_manual_changelog(list(filenames))

    if result_code == int(Status.SUCCESS.value):
        click.secho('Manual changelog check passed.', fg='green')
    else:
        ermsg = 'The changelog changed without a "build:" commit message.'
        raise click.ClickException(ermsg)

    return int(result_code)


@click.command(
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=False,
    name='check-type-from-status',
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='check-type-from-status',
)
@click.argument(
    'filenames',
    nargs=-1,
    type=click.Path(exists=False),
    help='Filenames to check',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.pass_context
@logging_call(logging.INFO, 'Checking commit type against staged files.')
def check_type_from_status_cli(
    ctx: click.Context,
    **kwargs: dict[str, Any],
) -> int:
    """Check the commit type against the staged files.

    Args:
        ctx: click context.
        kwargs: additional keyword arguments. Expected keys: filenames,
            nonexequi.

    Returns:
        0 if the commit type is compatible with the staged files; 1 otherwise.

    Examples:
        check-type-from-status .git/COMMIT_EDITMSG

    """
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.params.update(kwargs)
    filenames = ctx.params.get('filenames') or []
    nonexequi = ctx.params.get('nonexequi')

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        return int(Status.SUCCESS.value)

    result_code = check_type_from_status(list(filenames))

    if result_code == int(Status.SUCCESS.value):
        click.secho(
            'Commit type is compatible with the staged files.',
            fg='green',
        )
    else:
        ermsg = 'The commit type diverges from the staged files.'
        raise click.ClickException(ermsg)

    return int(result_code)


@click.group(
    name='githooks-cli',
    chain=True,
    context_settings=CONTEXT_SETTINGS_CLICK,
    no_args_is_help=True,
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='githooks-cli',
)
@click.option(
    '-N',
    '--nonexequi',
    default=False,
    is_flag=True,
    help='Do not run this hook.',
)
@click.option(
    '-v',
    '--verbose',
    is_flag=True,
    default=False,
    help='Enable verbose output',
)
@click.pass_context
def cli_group(ctx: click.Context, /, **kwargs: str) -> None:
    """Unifier Grouped for CLI - Command Line Interface."""
    ic(f'{kwargs=}\n{ctx.params=}')
    logging.warning(
        'callable=%s, command=%s, ctx.params=%s, kwargs=%s',
        inspect.stack()[0].function,
        ctx.command_path,
        ctx.params,
        kwargs,
    )
    ctx.ensure_object(dict)

    # Store in context
    nonexequi = ctx.params.get('nonexequi')
    verbose = ctx.params.get('verbose')

    if verbose:
        click.secho('Verbose mode active', fg='cyan')
        ic.enable()
    else:
        ic.disable()
        debug_enable()

    if nonexequi:
        click.secho(
            'Hook not executed due to the `--nonexequi` option.',
            fg='yellow',
        )
        ctx.exit(0)


cli_group.add_command(
    check_len_first_line_commit_msg_cli, name='check-len-first-line'
)
cli_group.add_command(check_type_commit_msg_cli, name='check-type-commit-msg')
cli_group.add_command(check_valid_branchname_cli, name='is-valid-branchname')
cli_group.add_command(check_valid_filenames_cli, name='is-valid-filename')
cli_group.add_command(clean_commit_msg_cli, name='clean-commit-msg')
cli_group.add_command(detect_private_key_cli, name='detect-key')
cli_group.add_command(effort_msg_cli, name='effort-msg')
cli_group.add_command(effort_random_msg_cli, name='effort-random-msg')
cli_group.add_command(footer_signedoffby_cli, name='set-footer-signed-off-by')
cli_group.add_command(insert_diff_cli, name='insert-diff-commit')
cli_group.add_command(check_commit_footer_cli, name='check-commit-footer')
cli_group.add_command(
    check_manual_changelog_cli, name='check-manual-changelog'
)
cli_group.add_command(check_manual_version_cli, name='check-manual-version')
cli_group.add_command(
    check_type_from_status_cli, name='check-type-from-status'
)
cli_group.add_command(pre_commit_installed_cli, name='is-precommit-installed')
cli_group.add_command(set_issue_from_branch_cli, name='set-issue-from-branch')
cli_group.add_command(set_type_from_status_cli, name='set-type-from-status')
cli_group.add_command(
    validate_format_commit_msg_cli, name='is-valid-msg-commit'
)

if __name__ == '__main__':
    sys.exit(cli_group(sys.argv[1:]))
