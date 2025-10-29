"""Module utils for project."""

from __future__ import annotations

import logging
import subprocess  # noqa: S404
from dataclasses import dataclass
from os import getenv

from icecream import ic

from incolume.py.githooks.rules import SUCCESS as SUCCESS
from incolume.py.githooks.rules import Status

ic.disable()


def debug_enable() -> bool:
    """Enable debug mode."""
    valid: list = ['1', 'true', 'on']
    debug: bool = any(
        getenv(x, '').casefold() in valid
        for x in ('INCOLUME_DEBUG_MODE', 'DEBUG_MODE', 'DEBUG')
    )

    ic.disable()  # Disable by default
    logging.debug(ic(f'{debug=}'))

    if debug:
        ic.enable()

    return debug


@dataclass
class Result:
    """Result dataclass for hooks this project."""

    code: Status = Status.SUCCESS
    message: str = ''


def get_branchname() -> str:
    """Get current branch name."""
    branch = (
        subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],  # noqa: S607
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
            ['git', 'diff', '--cached', '--name-status', '-r'],  # noqa: S607
            text=True,
        ).strip()
    except subprocess.CalledProcessError as e:  # pragma: no cover
        msg = 'Falha ao executar git diff'
        raise RuntimeError(msg) from e
