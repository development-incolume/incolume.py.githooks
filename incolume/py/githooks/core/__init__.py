"""Module utils for project."""

# ruff: noqa: S404 S607

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from os import getenv

from icecream import ic

from incolume.py.githooks.core.rules import SUCCESS as SUCCESS
from incolume.py.githooks.core.rules import Status

ic.disable()


def debug_var_active() -> bool:
    """Check environment variables for debug mode."""
    debug: bool = any(
        getenv(x, '').casefold() in {'1', 'true', 'on'}
        for x in ('INCOLUME_DEBUG_MODE', 'DEBUG_MODE', 'DEBUG')
    )

    logging.debug(ic(f'Var Debug Mode: {debug}'))

    return debug


def debug_enable() -> bool:
    """Enable debug mode."""
    debug: bool = debug_var_active()
    ic.disable()  # Disable by default

    if debug:
        ic.enable()
    logging.debug(ic(f'Debug mode {"enabled" if debug else "disabled"}.'))
    return debug


@dataclass
class Result:
    """Result dataclass for hooks this project."""

    code: Status = Status.SUCCESS
    message: str = ''


def get_signed_off_by() -> str:
    """Obtém a linha de assinatura 'Signed-off-by' do committer atual.

    Usa `git var GIT_COMMITTER_IDENT` para extrair o nome e email do committer.

    Returns:
        str: Linha formatada no padrão:
             "Signed-off-by: Nome <email>"

    Raises:
        RuntimeError: Se a execução do comando git falhar.

    """
    try:
        ident: str = subprocess.check_output(
            ['git', 'var', 'GIT_COMMITTER_IDENT'], text=True
        ).strip()
    except (
        subprocess.CalledProcessError
    ) as e:  # pragma: no cover; noqa: S110 TODO cover in future
        msg = 'Falha ao obter GIT_COMMITTER_IDENT'
        raise RuntimeError(msg) from e

    return f'Signed-off-by: {ident.split(">", maxsplit=1)[0]}>'


def get_branchname() -> str:
    """Get current branch name."""
    branch = (
        subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        )
        .strip()
        .decode('utf-8')
    )
    logging.debug(ic(branch))
    return branch


def get_git_diff() -> str:
    """Retorna a saída de `git diff --cached --name-status -r`."""
    try:
        return subprocess.check_output(
            ['git', 'diff', '--cached', '--name-status', '-r'],
            text=True,
        ).strip()
    except subprocess.CalledProcessError as e:  # pragma: no cover
        msg = 'Falha ao executar git diff'
        raise RuntimeError(msg) from e
