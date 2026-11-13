"""Check manual version bump in the commit message.

Rejeita uma mensagem de commit que nao comece com ``build:`` quando o
indice (staged) altera a versao do projeto: ``[project].version`` em
``pyproject.toml`` ou o valor de qualquer ``**/version.txt``. A
comparacao e sempre entre o indice e o ``HEAD``, nunca com a working
tree.

(c) Copyright 2026 incolume.com.br. All rights reserved.
"""

# ruff: file-ignore[suspicious-subprocess-import, subprocess-without-shell-equals-true, start-process-with-partial-path]

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover; Python < 3.11
    import tomli as tomllib  # type: ignore[no-redef]

from incolume.py.githooks.core.utils import find_project_root

BUILD_PREFIX: str = 'build:'
PYPROJECT: str = 'pyproject.toml'
VERSION_FILENAME: str = 'version.txt'


def _git(root: Path, *args: str) -> str | None:
    """Executa um comando git de leitura no repositorio.

    :param root: raiz do repositorio.
    :param args: argumentos do comando git.
    :return: saida do comando, ou None quando o caminho nao existe no
        commit ou no indice.

    .. versionadded:: 1.23.0
    """
    try:
        return subprocess.check_output(
            ['git', *args],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


def _staged_paths(root: Path) -> list[str]:
    """Lista os caminhos alterados no indice.

    :param root: raiz do repositorio.
    :return: caminhos relativos ao repositorio.

    .. versionadded:: 1.23.0
    """
    output = _git(root, 'diff', '--cached', '--name-only')
    return [line for line in (output or '').splitlines() if line]


def _project_version(content: str | None) -> str | None:
    """Extrai ``[project].version`` de um pyproject.toml.

    :param content: conteudo do arquivo, ou None se ausente.
    :return: versao declarada, ou None quando nao ha versao.

    .. versionadded:: 1.23.0
    """
    if content is None:
        return None
    try:
        return str(tomllib.loads(content)['project']['version'])
    except (KeyError, TypeError, tomllib.TOMLDecodeError):
        return None


def _version_file(content: str | None) -> str | None:
    """Normaliza o valor de um version.txt.

    :param content: conteudo do arquivo, ou None se ausente.
    :return: valor sem espacos nas pontas, ou None se ausente.

    .. versionadded:: 1.23.0
    """
    return None if content is None else content.strip()


def _staged_version_changed(root: Path, path: str) -> bool:
    """Compara a versao do indice com a versao do HEAD.

    :param root: raiz do repositorio.
    :param path: caminho relativo do arquivo de versao.
    :return: True se o valor da versao mudou no indice.

    .. versionadded:: 1.23.0
    """
    index = _git(root, 'show', f':{path}')
    head = _git(root, 'show', f'HEAD:{path}')
    if path == PYPROJECT:
        return _project_version(index) != _project_version(head)
    return _version_file(index) != _version_file(head)


def check_manual_version(
    filenames: list[str],
    repo_root: Path | str | None = None,
) -> int:
    """Validate that a version change is committed with a build message.

    :param filenames: arquivos de mensagem de commit.
    :param repo_root: raiz do repositorio; por padrao, o projeto atual.
    :return: 0 quando a mensagem e ``build:`` ou a versao nao mudou;
        1 caso contrario.

    .. versionadded:: 1.23.0
    """
    root = Path(repo_root) if repo_root else find_project_root(Path.cwd())
    messages = [
        Path(filename).read_text(encoding='utf-8') for filename in filenames
    ]
    if all(message.startswith(BUILD_PREFIX) for message in messages):
        return 0

    for staged in _staged_paths(root):
        path = staged.replace('\\', '/')
        if path != PYPROJECT and Path(path).name != VERSION_FILENAME:
            continue
        if _staged_version_changed(root, path):
            logging.critical(
                'Version changed in %s without a "build:" commit message.',
                path,
            )
            return 1

    return 0
