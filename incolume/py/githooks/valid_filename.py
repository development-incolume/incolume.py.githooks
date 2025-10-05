"""Hook to validate filenames."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from string import ascii_lowercase, digits

from icecream import ic

from incolume.py.githooks.rules import FAILURE, SNAKE_CASE, SUCCESS
from incolume.py.githooks.utils import Result, debug_enable

debug_enable()

SNAKE_CASE_REGEX = re.compile(SNAKE_CASE)


@dataclass
class ValidateFilename:
    """Rules for valid filename."""

    filename: Path | str = ''
    alphabet: str = ascii_lowercase + digits + '_áàãâéèêíìîóòõôúùûç'
    considers_underscore: bool = False
    code: int = field(default=SUCCESS, init=False)
    message: str = field(default='', init=False)

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
            Result(code=0, message='')
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
