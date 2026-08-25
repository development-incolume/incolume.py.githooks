"""Hook to validate filenames."""

from __future__ import annotations

import logging
import re
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_lowercase, digits

from icecream import ic

from incolume.py.githooks.core import debug_enable
from incolume.py.githooks.core.rules import (
    SNAKE_CASE,
    Result,
    Status,
)

with suppress(ImportError, ModuleNotFoundError):
    from typing import Self  # type: ignore[attr-defined]

with suppress(ImportError, ModuleNotFoundError):
    from typing_extensions import Self


debug_enable()

SNAKE_CASE_REGEX = re.compile(SNAKE_CASE)


@dataclass
class ValidateFilename:
    """Rules for valid filename."""

    filename: Path | str = ''
    alphabet: str = ascii_lowercase + digits + '_áàãâéèêíìîóòõôúùûç'
    considers_underscore: bool = True
    min_len: int = 3
    max_len: int = 256
    code: int = field(default=Status.SUCCESS, init=False)
    messages: list[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        """Post init."""
        self.filename = Path(self.filename)
        self.messages.append('')

    @property
    def refname(self) -> str:
        """Getting the reference name."""
        name = self.filename.stem  # type: ignore[union-attr]
        regex = r'[^a-z0-9_]' if self.considers_underscore else r'[^a-z0-9]'
        refname = re.sub(regex, '', name)
        ic(name, len(name), refname, len(refname), self.min_len, self.max_len)
        return refname

    def is_python_file(self, filename: Path | str = '') -> bool:
        """Check if the file is a Python file."""
        result = Path(filename or self.filename).suffix == '.py'
        msg = (
            f'{self.filename.as_posix()} {"Is" if result else "Not is"}'  # type: ignore[union-attr]
            ' Python file'
        )
        logging.debug(msg)
        return result

    def is_too_short(self) -> bool:
        """Check if the filename is too short."""
        result = self.is_python_file() and (len(self.refname) < self.min_len)
        msg = f'Name too short ({self.min_len=}): {self.filename}'
        if result:
            self.messages.append(f'\n[red]{msg}[/]')
            self.code |= Status.FAILURE
        return result

    def is_too_long(self) -> bool:
        """Check if the filename is too long."""
        result = self.is_python_file() and (len(self.refname) > self.max_len)
        msg = f'Name too long ({self.max_len=}): {self.filename}'
        if result:
            self.messages.append(f'\n[red]{msg}[/]')
            self.code |= Status.FAILURE
        return result

    def is_snake_case(self) -> bool:
        """Check if the filename is in snake_case."""
        result = (
            self.is_python_file()
            and SNAKE_CASE_REGEX.search(Path(self.filename).stem) is None
        )
        msg = f'Filename is not in snake_case: {self.filename}'
        if result:
            self.messages.append(f'\n[red]{msg}[/]')
            self.code |= Status.FAILURE
        return result

    def has_test_in_pathname(self) -> bool:
        """Check if the filename has 'test' or 'tests' in its name."""
        pathname = str(self.filename.parent)  # type: ignore[union-attr]
        return bool(re.match(r'^.*tests?.*$', str(pathname)))

    def is_valid_testing_filename(self) -> bool:
        """Check if the filename has 'test' or 'tests' in its name."""
        filename = self.filename.stem  # type: ignore[union-attr]
        rule1 = self.is_python_file() and self.has_test_in_pathname()
        rule2 = self.is_python_file() and re.match(
            r'^.*_tests?$', self.filename
        )
        rule3 = self.is_python_file() and re.match(
            r'^(?:(?!tests?).)*$', self.filename
        )

        if (not rule1 and rule2) or (rule1 and rule2) or not (rule1 and rule3):
            return True

        self.messages.append(
            '\n[red]Parece ser um arquivo de test.'
            f'\nTry: {Path("tests", re.sub(r"tests?", "", filename))}'
            '_test.py[/red]'
        )
        return False

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
        filename = Path(filename or self.filename)
        msg_return: str = ''
        code_return: Status = Status.SUCCESS
        path: Path = filename.parent
        basename: str = filename.stem

        msg = (
            f'{basename=}, {len(basename)=}, {self.refname=},'
            f'{len(self.refname)=}, {min_len=}, {max_len=}'
        )
        logging.debug(msg)

        if not self.is_python_file():
            return Result(code=Status.SUCCESS, message='')

        if len(self.refname) < min_len:
            msg_return += (
                f'\n[red]Name too short ({min_len=}): {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if len(self.refname) > max_len:
            msg_return += (
                f'\n[red]Name too long ({max_len=}): {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if SNAKE_CASE_REGEX.search(basename) is None:
            msg_return += (
                f'\n[red]Filename is not in snake_case: {filename}[/red]'
            )
            code_return |= Status.FAILURE

        if re.match(r'^.*tests?.*$', path.stem) and not re.match(
            r'.*_test$', basename
        ):
            msg_return += (
                f'\n[red]Filename should not be in a path: {filename}[/red]'
            )
            code_return |= Status.FAILURE

        return Result(code=code_return, message=msg_return)
