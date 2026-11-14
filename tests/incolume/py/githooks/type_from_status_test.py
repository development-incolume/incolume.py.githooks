"""Tests for the shared type-from-status heuristic."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from incolume.py.githooks import type_from_status
from incolume.py.githooks.core.rules import Status
from incolume.py.githooks.type_from_status import (
    deduce_type,
    get_staged_files,
    set_type_commit_msg,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestCaseDeduceType:
    """Heuristic precedence over staged paths."""

    @pytest.mark.parametrize(
        ['paths', 'expected'],
        [
            pytest.param(['pyproject.toml'], 'build'),
            pytest.param(['uv.lock'], 'build'),
            pytest.param(['incolume/py/githooks/version.txt'], 'build'),
            pytest.param(['CHANGELOG.md'], 'build'),
            pytest.param(['CHANGELOG.md', 'README.md'], 'docs'),
            pytest.param(['.github/workflows/ci.yml'], 'ci'),
            pytest.param(['tests/incolume/py/githooks/foo_test.py'], 'test'),
            pytest.param(['docs/hooks.md'], 'docs'),
            pytest.param(['README.md'], 'docs'),
            pytest.param(['mkdocs.yml'], 'docs'),
            pytest.param(
                ['incolume/py/githooks/prepare_commit_msg.py'], 'feat'
            ),
            pytest.param(['src/pkg/module.py'], 'feat'),
            pytest.param(['pyproject.toml', 'docs/hooks.md'], 'build'),
            pytest.param(
                ['.github/workflows/ci.yml', 'tests/pkg/x_test.py'], 'ci'
            ),
            pytest.param(['tests/pkg/x_test.py', 'docs/hooks.md'], 'test'),
            pytest.param(
                [
                    'docs/hooks.md',
                    'incolume/py/githooks/prepare_commit_msg.py',
                ],
                'feat',
            ),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py', 'pyproject.toml'],
                'feat',
            ),
            pytest.param([], ''),
            pytest.param(None, ''),
        ],
    )
    def test_deduce_type(self, paths: list[str] | None, expected: str) -> None:
        """Type follows the documented precedence."""
        assert deduce_type(paths) == expected


class TestCaseGetStagedFiles:
    """Staged files come from git, not from the branch."""

    def test_get_staged_files(self) -> None:
        """Split one staged path per line, ignoring blanks."""
        output = 'pyproject.toml\n\ndocs/hooks.md\n'
        with patch.object(
            type_from_status.subprocess,
            'check_output',
            return_value=output,
        ):
            assert get_staged_files() == [
                'pyproject.toml',
                'docs/hooks.md',
            ]

    def test_get_staged_files_empty(self) -> None:
        """Nothing staged yields an empty list."""
        with patch.object(
            type_from_status.subprocess,
            'check_output',
            return_value='',
        ):
            assert get_staged_files() == []

    def test_get_staged_files_without_git(self) -> None:
        """Outside a git repository there is nothing staged."""
        with patch.object(
            type_from_status.subprocess,
            'check_output',
            side_effect=FileNotFoundError,
        ):
            assert get_staged_files() == []


class TestCaseSetTypeCommitMsg:
    """Function level behaviour of the prepare-commit-msg helper."""

    def test_missing_commit_msg_file(self, tmp_path: Path) -> None:
        """A missing message file fails instead of being created."""
        result = set_type_commit_msg(tmp_path / 'COMMIT_EDITMSG')

        assert result.code == Status.FAILURE

    def test_empty_commit_msg_file(self, tmp_path: Path) -> None:
        """An empty template is left empty."""
        msg_file = tmp_path / 'COMMIT_EDITMSG'
        msg_file.write_text('\n', encoding='utf-8')

        result = set_type_commit_msg(
            msg_file, paths=['incolume/py/githooks/new_hook.py']
        )

        assert result.code == Status.SUCCESS
        assert msg_file.read_text(encoding='utf-8') == '\n'
