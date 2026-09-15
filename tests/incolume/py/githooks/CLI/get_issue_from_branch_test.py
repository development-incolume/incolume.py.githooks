"""Module test for get_issue_from_branch."""

from collections.abc import Generator
import shutil

from incolume.py.githooks.cli.get_issue_from_branch import main
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from inspect import stack


class TestCaseGetIssueFromBranch:
    """Test cases CLI main for get_issue_from_branch function."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    @pytest.fixture(scope='class')
    def filefortest(self) -> Generator[Path, None, None]:
        """Get the path to this file."""
        self.test_dir.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=self.test_dir) as tf:
            filename = Path(tf.name)
        filename.parent.mkdir(parents=True, exist_ok=True)
        filename.touch(exist_ok=True)
        yield filename
        shutil.rmtree(filename, ignore_errors=True)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(['', '', ''], '[ISSUE-195] ', marks=[]),
        ],
    )
    def test_get_issue_from_branch(
        self,
        filefortest: Generator[Path, None, None],
        entrance: list[str],
        expected: str,
    ) -> None:
        """Test get_issue_from_branch function."""
        flname = next(filefortest)
        entrance[1] = str(flname)
        main(entrance)
        assert flname.read_text() == expected
