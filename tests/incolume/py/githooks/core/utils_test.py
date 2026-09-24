"""Test module."""

import pytest
import incolume.py.githooks.core.utils as pkg


class TestCaseUtils:
    """Case test for utils."""

    @pytest.mark.parametrize(
        'entrance',
        [
            'pyproject.toml',
            '.git',
            'requirements.txt',
            'setup.cfg',
            '.venv',
        ],
    )
    def test_markers(self, entrance: str) -> None:
        """Markers values."""
        assert entrance in pkg.MARKERS
