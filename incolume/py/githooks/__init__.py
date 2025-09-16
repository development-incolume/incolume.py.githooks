"""Module githooks."""
# ruff: noqa: E501

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import Final

with suppress(ImportError, ModuleNotFoundError):
    import tomllib as tomli  # type: ignore[import]

with suppress(ImportError, ModuleNotFoundError):
    import tomli  # type: ignore[import]


REGEX_SEMVER: Final = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
RULE_BRANCHNAME: Final = r'^((enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9\-]+))$'
RULE_COMMITFORMAT = r'^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\(.*\))?\!?: #[0-9]+) .*(\n.*)*)$'

confproject = Path(__file__).parents[3] / 'pyproject.toml'
fileversion = Path(__file__).parent / 'version.txt'

with suppress(FileNotFoundError), confproject.open('rb') as f:
    fileversion.write_text(
        f'{tomli.load(f)["project"]["version"]!s}\n',
    )

__version__ = fileversion.read_text().strip()


class Result:
    """Result dataclass for hooks this project."""

    code: int
    message: str
