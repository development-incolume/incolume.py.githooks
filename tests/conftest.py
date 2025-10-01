"""Module to configure the test suite."""

import pytest
from click.testing import CliRunner

from incolume.py.githooks.rules import REGEX_SEMVER

__author__ = '@britodfbr'  # pragma: no cover


@pytest.fixture(scope='session')
def semver_regex() -> str:
    """Fixture para regex de validação do Versionamento Semântico."""
    return REGEX_SEMVER


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture to CliRunner."""
    return CliRunner()
