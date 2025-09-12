"""Module to configure the test suite."""

import re

import pytest
from click.testing import CliRunner

__author__ = '@britodfbr'  # pragma: no cover


@pytest.fixture(scope='session')
def semver_regex() -> str:
    """Fixture para regex de validação do Versionamento Semântico."""
    return re.escape(r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$')


@pytest.fixture
def cli_runner() -> CliRunner:
    """Fixture to CliRunner."""
    return CliRunner()
