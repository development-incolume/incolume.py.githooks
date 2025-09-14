"""Módulo de testes."""

import re

import pytest
from icecream import ic

from incolume.py.githooks import REGEX, __version__


@pytest.mark.fasttest
class TestSemVer:
    """Test case class for Sematic Versions."""

    def test_version(self, semver_regex: str) -> None:
        """Validação de versionamento semântico para versão do pacote."""
        assert ic(re.fullmatch(semver_regex, __version__, re.IGNORECASE))

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(__version__, True, marks=[pytest.mark.fasttest]),
            pytest.param('1', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.0', False, marks=[pytest.mark.fasttest]),
            pytest.param('0.1', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1-rc0', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1-rc-0', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1-dev0', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1-a0', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1a.0', False, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1-a.0', True, marks=[pytest.mark.fasttest]),
            pytest.param('0.0.1', True, marks=[pytest.mark.fasttest]),
            pytest.param('0.1.0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1-rc.0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1-dev.0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1-dev.1', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1-dev.2', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.0.1-alpha.0', True, marks=[pytest.mark.fasttest]),
            pytest.param(
                '1.0.1-alpha.266',
                True,
                marks=[pytest.mark.fasttest],
            ),
            pytest.param('1.0.1-beta.0', True, marks=[pytest.mark.fasttest]),
            pytest.param(
                '1.1.1-alpha.99999',
                True,
                marks=[pytest.mark.fasttest],
            ),
            pytest.param(
                '11111.1.1-rc.99999',
                True,
                marks=[pytest.mark.fasttest],
            ),
            pytest.param('1.1.99999', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.999999.1', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1a0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1rc0', True, marks=[pytest.mark.fasttest]),
            pytest.param('1.1.1rc1111', True, marks=[pytest.mark.fasttest]),
        ],
    )
    def test_semantic_version(
        self,
        *,
        entrance: str,
        expected: bool,
    ) -> None:
        """Test semantic version asserts."""
        assert (
            bool(
                re.fullmatch(
                    REGEX,
                    entrance,
                    flags=re.IGNORECASE,
                ),
            )
            == expected
        )
