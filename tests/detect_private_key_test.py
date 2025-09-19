"""Test for detect_private_key hook."""

from __future__ import annotations
from inspect import stack
from pathlib import Path
import shutil
from typing import NoReturn
from incolume.py.githooks.detect_private_key import has_private_key
from icecream import ic
from tempfile import gettempdir
import pytest


class TestCaseDetectPrivateKey:
    """Test case for detect_private_key hook."""

    test_dir = Path(gettempdir()) / 'TestCaseDetectPrivateKey'

    def setup_method(self, method) -> None:
        """Setup method.

        Cria a estrutura em arvore de diretórios necessários para os testes.
        """
        ic(f'starting execution ({method.__name__}) of {stack()[0][3]}')

        self.test_dir.mkdir(parents=True, exist_ok=True)

    def teardown_method(self, method) -> None:
        """Teardown method.

        Remove a arvore de diretórios criadas após os testes realizados.
        """
        ic(f'finished execution ({method.__name__}) of {stack()[0][3]}')
        shutil.rmtree(self.test_dir)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('test_no_key.txt', '', marks=[]),
            pytest.param(
                'test_no_key.txt', '', marks=[pytest.mark.xfail(strict=False)]
            ),
        ],
    )
    def test_no_private_key(self, entrance, expected) -> NoReturn:
        """Test with a file that does not contain a private key."""
        test_file = self.test_dir / entrance
        test_file.write_text('This is a test file without any private keys.\n')
        ic(test_file)

        assert has_private_key(test_file)
