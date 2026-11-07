"""Module test for get_issue_from_branch."""

from collections.abc import Generator
import inspect
import shutil
from incolume.py.githooks.core import subprocess
from unittest.mock import patch
from incolume.py.githooks.cli.cli import set_issue_from_branch_cli
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from inspect import stack
from click.testing import CliRunner
from icecream import ic


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

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class.

        Remove a arvore de diretórios criadas após os testes realizados.
        """
        ic(f'teardown for {cls.__name__}')
        for dout in (d for d in dir(cls) if d.startswith('test_')):
            ic(f'{dout=}')
            shutil.rmtree(cls.test_dir / dout, ignore_errors=True)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                ['', ''],
                '[ISSUE-123] ',
                marks=[
                    pytest.mark.runner_setup(
                        charset='utf-8', env={'test': 1}, echo_stdin=True
                    )
                ],
            ),
            pytest.param(
                ['COMMIT_EDITMSG', ''],
                '[ISSUE-123] ',
                marks=[
                    pytest.mark.runner_setup(
                        charset='cp1251', env={'test': 2}, echo_stdin=True
                    )
                ],
            ),
        ],
        scope='class',
    )
    def test_get_issue_from_branch(
        self,
        isolated_cli_runner: CliRunner,
        filefortest: Path,
        entrance: list[str],
        expected: str,
    ) -> None:
        """Test get_issue_from_branch function."""
        flin: Path = filefortest
        if entrance[0]:
            flin = self.test_dir / inspect.stack()[0][3] / entrance[0]
            flin.parent.mkdir(parents=True, exist_ok=True)
            flin.touch(exist_ok=True)
        entrance[0] = str(flin)

        with patch.object(
            subprocess,
            'check_output',
            return_value=bytes('123-fake-commit-message', 'utf-8'),
        ):
            result = isolated_cli_runner.invoke(
                set_issue_from_branch_cli, entrance
            )
            assert result.exit_code == 0
            # assert 'Adicionado o número do ticket 123 à mensagem de commit.' in result.output
            assert flin.read_text(encoding='utf-8') == expected
