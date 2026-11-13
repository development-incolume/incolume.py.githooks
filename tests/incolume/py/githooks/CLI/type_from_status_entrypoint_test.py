"""Entry-point wiring for the set-type-from-status hook."""

# ruff: file-ignore[suspicious-subprocess-import]

from __future__ import annotations

import shutil
import subprocess
from typing import TYPE_CHECKING

from incolume.py.githooks.cli import cli

if TYPE_CHECKING:
    from click.testing import CliRunner

COMMAND = 'set-type-from-status'


class TestCaseSetTypeFromStatusEntryPoint:
    """The console script exists and answers with exit code 0."""

    def test_console_script_help(self) -> None:
        """The installed entry point runs and prints its help."""
        executable = shutil.which(COMMAND)
        assert executable, f'entry point {COMMAND} is not installed'

        result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
            [executable, '--help'],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0
        assert COMMAND in result.stdout

    def test_githooks_cli_subcommand(self, cli_runner: CliRunner) -> None:
        """The grouped CLI exposes the same command by exit code."""
        result = cli_runner.invoke(cli.cli_group, [COMMAND, '--help'])

        assert result.exit_code == 0
        assert COMMAND in result.output
