"""Hook to validate filenames."""

from __future__ import annotations

import re
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_lowercase, digits

from icecream import ic

from incolume.py.githooks.rules import FAILURE, SNAKE_CASE, SUCCESS
from incolume.py.githooks.utils import Result, debug_enable

with suppress(ImportError, ModuleNotFoundError):
    from typing import Self  # type: ignore[import]

with suppress(ImportError, ModuleNotFoundError):
    from typing_extensions import Self  # type: ignore[import]


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
    code: int = field(default=SUCCESS, init=False)
    message: str = field(default='', init=False)

    def __post_init__(self) -> None:
        """Post init."""
        self.filename = Path(self.filename)

    @property
    def refname(self) -> str:
        """Get the reference name."""
        name = self.filename.stem
        regex = r'[^a-z0-9_]' if self.considers_underscore else r'[^a-z0-9]'
        refname = re.sub(regex, '', name)
        ic(name, len(name), refname, len(refname), self.min_len, self.max_len)
        return refname

    def __is_python_file(self) -> bool:
        """Check if the file is a Python file."""
        return self.filename.suffix == '.py'

    def is_too_short(self) -> Self:
        """Check if the filename is too short."""
        if self.__is_python_file() and (len(self.refname) < self.min_len):
            self.message += (
                f'\n[red]Name too short ({self.min_len=}): {self.filename}[/]'
            )
            self.code |= FAILURE
        return self

    def is_too_long(self) -> Self:
        """Check if the filename is too long."""
        if self.__is_python_file() and (len(self.refname) > self.max_len):
            self.message += (
                f'\n[red]Name too long ({self.max_len=}): {self.filename}[/]'
            )
            self.code |= FAILURE
        return self

    def is_snake_case(self) -> Self:
        """Check if the filename is in snake_case."""
        if (
            self.__is_python_file()
            and SNAKE_CASE_REGEX.search(self.filename.stem) is None
        ):
            self.message += (
                f'\n[red]Filename is not in snake_case: {self.filename}[/]'
            )
            self.code |= FAILURE
        return self

    def __has_test_in_pathname(self) -> Self:
        """Check if the filename has 'test' or 'tests' in its name."""
        pathname = str(self.filename.parent)
        return bool(re.match(r'^.*tests?.*$', str(pathname)))

    def has_testing_in_filename(self) -> Self:
        """Check if the filename has 'test' or 'tests' in its name."""
        filename = self.filename.stem
        if (
            self.__is_python_file()
            and self.__has_test_in_pathname()
            and not re.match(r'^.*_test$', filename)
        ):
            self.code |= re.match(r'^.*_tests?$', filename) is None
            self.code |= re.match(r'^(?:(?!tests?).)*$', filename) is not None
            self.message += (
                '\n[red]Parece ser um arquivo de test.'
                f'\nTry: {Path("tests", filename + "_test.py")}[/red]'
            )
        return self

    @staticmethod
    def is_valid(
        filename: str | Path, min_len: int = 3, max_len: int = 256
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
            >>> ValidateFilename.is_valid('valid_name.py')
            Result(code=<Status.SUCCESS: 0>, message='')
            >>> ValidateFilename.is_valid('sh.py', min_len=3)
            Result(code=1, message='\n[red]Name too short (min_len=3): sh.py[/]')

        """  # noqa: E501
        filename = Path(filename)
        msg_return = ''
        code_return = SUCCESS
        path = filename.parent
        name = filename.stem

        refname = re.sub(r'[^a-z0-9]', '', name)
        ic(name, len(name), refname, len(refname), min_len, max_len)

        if len(refname) < min_len:
            msg_return += f'\n[red]Name too short ({min_len=}): {filename}[/]'
            code_return |= FAILURE

        if len(refname) > max_len:
            msg_return += f'\n[red]Name too long ({max_len=}): {filename}[/]'
            code_return |= FAILURE

        if SNAKE_CASE_REGEX.search(name) is None:
            msg_return += (
                f'\n[red]Filename is not in snake_case: {filename}[/]'
            )
            code_return |= FAILURE

        if re.match(r'^.*tests?.*$', path.stem) and not re.match(
            r'.*_test$', name
        ):
            msg_return += (
                f'\n[red]Filename should not be in a path: {filename}[/]'
            )

        return Result(code=code_return, message=msg_return)
