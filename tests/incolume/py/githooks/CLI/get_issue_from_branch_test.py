"""Module test for get_issue_from_branch."""

from collections.abc import Generator
import shutil

from incolume.py.githooks.cli.get_issue_from_branch import main
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from inspect import stack


@pytest.fixture(scope='class')
def filefortest(request: pytest.FixtureRequest) -> Generator[Path, None, None]:
    """Get the path to this file."""
    request.cls.test_dir.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=request.cls.test_dir) as tf:
        filename = Path(tf.name)
    filename.parent.mkdir(parents=True, exist_ok=True)
    filename.touch(exist_ok=True)
    yield filename
    shutil.rmtree(filename, ignore_errors=True)


class TestCaseGetIssueFromBranch:
    """Test cases CLI main for get_issue_from_branch function."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(['', '', ''], '[ISSUE-195] ', marks=[]),
            pytest.param(
                ['', test_dir / 'COMMIT_EDITMSG', ''], '[ISSUE-195] ', marks=[]
            ),
        ],
        scope='class',
    )
    def test_get_issue_from_branch(
        self,
        filefortest: Path,
        entrance: list[str],
        expected: str,
    ) -> None:
        """Test get_issue_from_branch function."""
        flin: Path | None = None
        if entrance[1]:
            flin: Path = Path(entrance[1])
            flin.parent.mkdir(parents=True, exist_ok=True)
            flin.touch(exist_ok=True)
        entrance[1] = str(flin) or None
        main(entrance)
        assert flin.read_text(encoding='utf-8') == expected
