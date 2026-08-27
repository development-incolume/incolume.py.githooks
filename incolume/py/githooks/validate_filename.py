"""Hook to validate filenames."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from string import ascii_lowercase, digits

from deprecated import deprecated
from icecream import ic

from incolume.py.githooks.core import debug_enable
from incolume.py.githooks.core.rules import (
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
PolicyFn = Callable[[RequestFl], RequestFl]


def apply_policies(
    filename: Path, request: RequestFl, policies: list[PolicyFn]
) -> RequestFl:
    """Apply policies."""
    return reduce(
        lambda current, policy: policy(filename, current), policies, request
    )


def rule_filename_notnull(filename: Path, request: RequestFl) -> RequestFl:
    """Rule for match filename.

    Return True if filename is not null.
    """
    ic(self.refname)
    return bool(self.refname)


def rule_is_python_file() -> bool:
    """Rule for match filename.

    Return True if filename is a python file.
    """
    return Path(self.filename).suffix == '.py'


def rule_not_started_with_number() -> bool:
    """Rule for match filename.

    Return True if not start with number.
    """
    return bool(re.match(r'[^0-9][a-zA-Z0-9_]*', Path(self.filename).stem))


def rule_has_test_into_filename() -> bool:
    """Rule for match filename.

    Return True if filename has test into filename.
    """
    return not bool(re.match(r'^(?:(?!tests?).)*$', str(self.filename)))


def rule_has_test_in_pathname() -> bool:
    """Check if the filename has 'test' or 'tests' in its name."""
    pathname: str = str(self.filename.parent)  # type: ignore[union-attr]
    return bool(re.match(r'^.*tests?.*$', pathname))


def rule_is_dundle_init() -> bool:
    """Check if is dundler init file."""
    result = re.match(r'^__init__.py$', Path(self.filename).name)
    ic(result)
    return bool(result)


def rule_has_filename_ends_with_test() -> bool:
    """Check if filename ends with test."""
    return bool(re.match(r'^.*_tests?$', Path(self.filename).stem))


@deprecated(reason='Deprecated, will be removed coming soon.', version='1.10.0a39')
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

    def __is_python_file(self) -> bool:
        """Check if the file is a Python file."""
        result = self.filename.suffix == '.py'  # type: ignore[union-attr]
        msg = (
            f'{self.filename.as_posix()} {"Is" if result else "Not is"}'  # type: ignore[union-attr]
            ' Python file'
        )
        logging.debug(msg)
        return result

    def is_too_short(self) -> Self:
        """Check if the filename is too short."""
        if self.__is_python_file() and (len(self.refname) < self.min_len):
            self.message += (
                f'\n[red]Name too short ({self.min_len=}): {self.filename}[/]'
            )
            self.code |= Status.FAILURE
        return self

    def is_too_long(self) -> Self:
        """Check if the filename is too long."""
        if self.__is_python_file() and (len(self.refname) > self.max_len):
            self.message += (
                f'\n[red]Name too long ({self.max_len=}): {self.filename}[/]'
            )
            self.code |= Status.FAILURE
        return self

    def is_snake_case(self) -> Self:
        """Check if the filename is in snake_case."""
        if (
            self.__is_python_file()
            and SNAKE_CASE_REGEX.search(self.filename.stem) is None  # type: ignore[union-attr]
        ):
            self.message += (
                f'\n[red]Filename is not in snake_case: {self.filename}[/]'
            )
            self.code |= Status.FAILURE
        return self

    def __has_test_in_pathname(self) -> Self:
        """Check if the filename has 'test' or 'tests' in its name."""
        pathname = str(self.filename.parent)  # type: ignore[union-attr]
        return bool(re.match(r'^.*tests?.*$', str(pathname)))

    def has_testing_in_filename(self) -> Self:
        """Check if the filename has 'test' or 'tests' in its name."""
        filename = self.filename.stem  # type: ignore[union-attr]
        if (
            self.__is_python_file()
            and self.__has_test_in_pathname()
            and not re.match(r'^.*_test$', filename)
        ):
            self.code |= re.match(r'^.*_tests?$', filename) is None
            self.code |= re.match(r'^(?:(?!tests?).)*$', filename) is not None
            self.message += (
                '\n[red]Parece ser um arquivo de test.'
                f'\nTry: {Path("tests", re.sub(r"tests?", "", filename))}'
                '_test.py[/red]'
            )
        return self

    def is_valid(
        self: Self,
        filename: str | Path = '',
        min_len: int = 3,
        max_len: int = 256,
    ) -> Result:
        r"""Check if a filename is valid.

        A valid filename is in snake_case and has at least `min_len` characters.
        extract the name so that `/my/repo/x.py` becomes `x`

        Args:
            filename: The filename to check.
            min_len: Minimum length of the filename (default: 3).
            max_len: Maximum length of the filename (default: 256).

        Returns:
            Result: The result of the check.

        Examples:
            >>> ValidateFilename().is_valid('valid_name.py')
            Result(code=<Status.SUCCESS: 0>, message='')
            >>> ValidateFilename().is_valid('sh.py', min_len=3)
            Result(code=<Status.FAILURE: 1>, message='\n[red]Name too short (min_len=3): sh.py[/]')

        """  # ruff: ignore[line-too-long]
        filename = Path(filename)
        msg_return: str = ''
        code_return: Status = Status.SUCCESS
        path: Path = filename.parent
        name: str = filename.stem

        refname = re.sub(r'[^a-z0-9]', '', name)
        msg = (
            f'{name=}, {len(name)=}, {refname=},'
            f'{len(refname)=}, {min_len=}, {max_len=}'
        )
        logging.debug(msg)

        if not self.__is_python_file():
            return Result(code=Status.SUCCESS, message='')

        if len(refname) < min_len:
            msg_return += (
                f'\n[red]Name too short ({min_len=}): {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if len(refname) > max_len:
            msg_return += (
                f'\n[red]Name too long ({max_len=}): {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if SNAKE_CASE_REGEX.search(name) is None:
            msg_return += (
                f'\n[red]Filename is not in snake_case: {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if re.match(r'^.*tests?.*$', path.stem) and not re.match(
            r'.*_test$', name
        ):
            msg_return += (
                f'\n[red]Filename should not be in a path: {filename}[/red]'
            )
            code_return |= Status.FAILURE

        return Result(code=code_return, message=msg_return)
