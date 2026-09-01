"""Hook to validate filenames."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field, replace
from functools import reduce
from inspect import stack
from pathlib import Path
from string import ascii_lowercase, digits

from deprecated import deprecated
from icecream import ic

from incolume.py.githooks.core import debug_enable
from incolume.py.githooks.core.rules import (
    FILENAME_STRUCTURE,
    SNAKE_CASE,
    RequestFl,
    Result,
    Status,
)

with suppress(ImportError, ModuleNotFoundError):
    from typing import Self  # type: ignore[attr-defined]

with suppress(ImportError, ModuleNotFoundError):
    from typing_extensions import Self


debug_enable()

SNAKE_CASE_REGEX = re.compile(SNAKE_CASE)
FILENAME_STRUCTURE_REGEX = re.compile(FILENAME_STRUCTURE)

PolicyFn = Callable[[RequestFl], RequestFl]


def apply_policies(request: RequestFl, policies: list[PolicyFn]) -> RequestFl:
    """Apply policies."""
    return reduce(lambda current, policy: policy(current), policies, request)


def audit(request: RequestFl) -> RequestFl:
    """Register for auditory."""
    if not request.requires_audit:
        return request
    return replace(
        request,
        audit_log=[
            *request.audit_log,
            f'{request.filename} performed on `{request.action}`',
        ],
    )


def rule_filename_structure(request: RequestFl) -> RequestFl:
    """Rule for structure filename."""
    request.action = stack()[0][3]
    structure_fail = FILENAME_STRUCTURE_REGEX.search(request.filename.name)

    if bool(structure_fail):
        return request
    request.code |= Status.FAILURE
    request.messages.append('Filename structure is invalid.')
    return request


def rule_filename_notnull(request: RequestFl) -> RequestFl:
    """Rule for match filename.

    Return True if filename is not null.
    """
    request.action = stack()[0][3]
    ic(request.refname)
    if bool(request.refname) or request.has_filename:
        return request
    request.code |= Status.FAILURE
    request.messages.append('Null Filename is invalid.')

    return request


def rule_not_started_with_number(request: RequestFl) -> RequestFl:
    """Rule for match filename.

    Return True if not start with number.
    """
    request.action = stack()[0][3]
    if bool(re.match(r'[^0-9][a-zA-Z0-9_]*', request.filename.stem)):
        return request
    request.code |= Status.FAILURE
    request.messages.append('Filename started with number is invalid.')
    return request


def rule_has_filename_ends_with_test(request: RequestFl) -> RequestFl:
    """Check if filename ends with test."""
    request.action = stack()[0][3]

    if (request.is_python_file and request.is_not_test_filename) or (
        request.has_test_pathname
        and bool(re.match(r'^.*_tests?$', request.filename.stem))
    ):
        return request
    request.code |= Status.FAILURE
    request.messages.append(
        'It appears to be a test file outside the test directory.'
    )
    return request


@deprecated(reason='deprecated in favor of `rule_lenght`', version='1.10.0a40')
def rule_too_short(request: RequestFl) -> RequestFl:
    """Check if the filename is too short."""
    request = rule_filename_notnull(request)
    if request.is_python_file and (len(request.refname) >= request.min_len):
        return request

    request.code |= Status.FAILURE
    request.messages.append(
        f'Filename too short ({request.min_len}+): {request.filename.name}'
    )
    return request


@deprecated(reason='deprecated in favor of `rule_lenght`', version='1.10.0a40')
def rule_too_long(request: RequestFl) -> RequestFl:
    """Check if the filename is too long."""
    request = rule_filename_notnull(request)
    if request.is_python_file and (len(request.refname) <= request.max_len):
        return request

    request.code |= Status.FAILURE
    request.messages.append(
        f'Filename too long ({request.max_len}-): {request.filename.name}'
    )
    return request


def rule_length(request: RequestFl) -> RequestFl:
    """Check if the filename is too short."""
    request.action = stack()[0][3]
    request = rule_filename_notnull(request)
    length = len(request.refname)
    if request.is_python_file and (
        request.min_len <= length <= request.max_len
    ):
        return request

    request.code |= Status.FAILURE
    if length < request.min_len:
        request.messages.append(
            f'Filename too short ({request.min_len}+): {request.filename.name}'
        )
    if length > request.max_len:
        request.messages.append(
            f'Filename too long ({request.max_len}-): {request.filename.name}'
        )
    return request


def rule_snake_case(request: RequestFl) -> RequestFl:
    """Check if the filename is in snake_case."""
    request.action = stack()[0][3]
    if not request.is_python_file or (
        request.is_python_file
        and SNAKE_CASE_REGEX.search(request.filename.stem)
    ):
        return request

    request.code |= Status.FAILURE
    request.messages.append(
        f'Filename is not in snake_case: {request.filename.name}'
    )
    return request


def validate_filename(
    filename: str, **kwargs: dict[str, str | Path]
) -> RequestFl:
    """Check if a filename is valid.

    A valid filename is in snake_case and has at least `min_len` characters.
    extract the name so that `/my/repo/x.py` becomes `x`

    Args:
      filename (Path | str): Filename to check;
      kwargs:
        min_len (int): Minimum length of the filename (default: 3);
        max_len (int): Maximum length of the filename (default: 256);
        considers_underscore (bool): If consider
              underscore in filename (default: True);

    Returns:
        Result: The result of the check.

    Examples:
        >>> validate_filename('module/valid_name.py')
        RequestFl(filename=WindowsPath('module/valid_name.py'), alphabet='abcdefghijklmnopqrstuvwxyz0123456789_áàãâéèêíìîóòõôúùûç', considers_underscore=True, min_len=3, max_len=256, requires_audit=False, required_role=None, action='rule_has_filename_ends_with_test', audit_log=[''], code=<Status.SUCCESS: 0>, messages=[''])

    """  # ruff:ignore[line-too-long]
    flname: Path = Path(filename or kwargs.get('filename', ''))  # type: ignore[arg-type]
    min_len = kwargs.get('min_len', 3)
    max_len = kwargs.get('max_len', 256)
    considers_underscore = kwargs.get('considers_underscore', True)
    request: RequestFl = RequestFl(
        flname,
        min_len=min_len,
        max_len=max_len,
        considers_underscore=considers_underscore,
    )

    policies: list[PolicyFn] = [
        rule_filename_notnull,
        rule_snake_case,
        rule_length,
        rule_not_started_with_number,
        rule_has_filename_ends_with_test,
    ]

    request = rule_filename_structure(request)
    if not request.is_python_file and request.code is Status.SUCCESS:
        return request

    request = apply_policies(request, policies)
    logging.debug(request)

    return request


@deprecated(
    reason='Deprecated, will be removed coming soon.', version='1.10.0a39'
)
@dataclass
class ValidateFilename:
    """Rules for valid filename."""

    filename: Path | str = ''
    alphabet: str = ascii_lowercase + digits + '_áàãâéèêíìîóòõôúùûç'
    considers_underscore: bool = True
    min_len: int = 3
    max_len: int = 256
    code: int = field(default=Status.SUCCESS, init=False)
    message: str = field(default='', init=False)

    def __post_init__(self) -> None:
        """Post init."""
        self.filename = Path(self.filename)

    @property
    def refname(self) -> str:
        """Getting the reference name."""
        name = self.filename.stem  # type: ignore[union-attr]
        regex = r'[^a-z0-9_]' if self.considers_underscore else r'[^a-z0-9]'
        refname = re.sub(regex, '', name)
        ic(name, len(name), refname, len(refname), self.min_len, self.max_len)
        return refname
