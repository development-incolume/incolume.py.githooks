"""Module test for get_issue_from_branch."""

from collections.abc import Callable, Generator
import shutil

from incolume.py.githooks.cli.get_issue_from_branch import main
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from inspect import stack


class TestCaseGetIssueFromBranch:
    """Test cases CLI main for get_issue_from_branch function."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    def setup_teardown_method(self, method: Callable[[], None]) -> None:
        """Set method.

        Cria a estrutura em arvore de diretórios necessários para os testes.
        """
        path = self.test_dir / method.__name__
        path.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=path) as tf:
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
        entrance: list[str],
        expected: str,
    ) -> None:
        """Test get_issue_from_branch function."""
        flname = next(filefortest)
        entrance[1] = str(flname)
        main(entrance)
        assert flname.read_text() == expected
