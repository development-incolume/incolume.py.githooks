"""Test for detect_private_key hook."""

from __future__ import annotations
from pathlib import Path
import shutil
from typing import NoReturn, Callable
from incolume.py.githooks.detect_private_key import (
    has_private_key,
    BLACKLIST,
    SUCCESS,
    FAILURE,
    main,
)
from icecream import ic
from tempfile import gettempdir, NamedTemporaryFile
import pytest


class TestCaseDetectPrivateKey:
    """Test case for detect_private_key hook."""

    test_dir = Path(gettempdir()) / 'TestCaseDetectPrivateKey'

    def setup_method(self, method: Callable) -> None:
        """Set method.

        Cria a estrutura em arvore de diretórios necessários para os testes.
        """
        ic(f'setup for {method.__name__}')
        self.test_dir.mkdir(parents=True, exist_ok=True)

    def teardown_method(self, method: Callable) -> None:
        """Teardown method.

        Remove a arvore de diretórios criadas após os testes realizados.
        """
        ic(f'teardown for {method.__name__}')
        shutil.rmtree(self.test_dir)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('test_no_key.txt', SUCCESS, marks=[]),
            pytest.param(
                'test_no_key.py',
                SUCCESS,
                marks=[pytest.mark.xfail(strict=False)],
            ),
        ],
    )
    def test_no_private_key(self, entrance, expected) -> NoReturn:
        """Test with a file that does not contain a private key."""
        test_file = self.test_dir / entrance
        test_file.write_text('This is a test file without any private keys.\n')
        ic(test_file)

        assert has_private_key(test_file) is expected

    @pytest.mark.parametrize(
        'entrance', [pytest.param(line, marks=[]) for line in BLACKLIST]
    )
    def test_with_private_key(self, entrance) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_private_key.txt'
        test_file.write_text(f'----- {entrance} -----\n')
        assert has_private_key(test_file) is FAILURE

    @pytest.mark.parametrize(
        'entrance', [pytest.param(line, marks=[]) for line in BLACKLIST]
    )
    def test_main(self, capsys, entrance) -> NoReturn:
        """Test CLI."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)

        ic(test_file, type(test_file))
        test_file.write_bytes(f'----- {entrance} -----\n'.encode())
        main([test_file.as_posix()])
        captured = capsys.readouterr()
        assert f'Private key found: {test_file.as_posix()}' in captured.out

    def test_has_rsa_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_RSA_key.txt'
        test_file.write_text(
            '-----BEGIN RSA PRIVATE KEY-----\n'
            'MIIEpAIBAAKCAQEA7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v5y5v5y5v5y5v\n'
            '-----END RSA PRIVATE KEY-----\n'
        )

        assert has_private_key(test_file) is FAILURE

    def test_has_dsa_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_DSA_key'
        test_file.write_text(
            '-----BEGIN DSA PRIVATE KEY-----\n'
            'MIIBuwIBAAKBgQDc5g5h5y5v5y5v5y5v5y5v5y5v5y5v5y5v5y5v\n'
            '-----END DSA PRIVATE KEY-----\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_ec_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_EC_key.txt'
        test_file.write_text(
            '-----BEGIN EC PRIVATE KEY-----\n'
            'MHcCAQEEIO7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v'
            '-----END EC PRIVATE KEY -----\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_openssh_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_OpenSSH_key.txt'
        test_file.write_text(
            '-----BEGIN OPENSSH PRIVATE KEY-----\n'
            'b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gt'
            'cnNhAAAAAwEAAQAAAQEArw7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v5y5v5y5v\n'
            '-----END OPENSSH PRIVATE KEY-----\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_pgp_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_PGP_key.txt'
        test_file.write_text(
            '-----BEGIN PGP PRIVATE KEY BLOCK-----\n'
            'Version: GnuPG v1.4.11 (GNU/Linux)\n'
            '\n'
            'lQO+BFezvYkBCADL5g5h5y5v5y5v5y5v5y5v5y5v5y5v5y5v\n'
            '=abcd\n'
            '-----END PGP PRIVATE KEY BLOCK-----\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_putty_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_PuTTY_key.txt'
        test_file.write_text(
            'PuTTY-User-Key-File-2: ssh-rsa\n'
            'Encryption: none\n'
            'Comment: rsa-key-20240406\n'
            'Public-Lines: 6\n'
            'AAAAB3NzaC1yc2EAAAABJQAAAQEArw7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v5y5v\n'
            'Private-Lines: 14\n'
            'AAABAQC7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v5y5v\n'
            'Private-MAC: abcd1234abcd1234abcd1234abcd1234abcd1234\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_ssh2_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_SSH2_key.txt'
        test_file.write_text(
            '---- BEGIN SSH2 ENCRYPTED PRIVATE KEY ----\n'
            'Comment: "rsa-key-20240406"\n'
            'Proc-Type: 4,ENCRYPTED\n'
            'DEK-Info: AES-128-CBC,abcd1234abcd1234\n'
            '\n'
            'AAABAQC7r+6G9k5g5h5y5v5y5v5y5v5y5v5y5v5y5v\n'
            '---- END SSH2 ENCRYPTED PRIVATE KEY ----\n'
        )
        assert has_private_key(test_file) is FAILURE

    def test_has_openvpn_key(self) -> NoReturn:
        """Test with a file that contains a private key."""
        test_file = self.test_dir / 'with_OpenVPN_key.txt'
        test_file.write_text(
            '-----BEGIN OpenVPN Static key V1-----\n'
            'abcd1234abcd1234abcd1234abcd1234\n'
            '-----END OpenVPN Static key V1-----\n'
        )
        assert has_private_key(test_file) is FAILURE
