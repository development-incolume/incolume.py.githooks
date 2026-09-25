"""Module core.utils."""

# ruff: file-ignore[suspicious-subprocess-import, start-process-with-partial-path]

import itertools
import shutil
import subprocess
from pathlib import Path
from typing import Final

MARKERS: Final[tuple[str, ...]] = (
    'pyproject.toml',
    '.git',
    'requirements.txt',
    'setup.cfg',
    '.venv',
)


def backup_file(filename: Path, ext: str = '.bkp', start: int = 1) -> Path:
    """Backup file."""
    count = itertools.count(start=start)
    backup: Path = filename.with_suffix(filename.suffix + ext)

    while backup.is_file():
        backup = filename.with_suffix(filename.suffix + f'{ext}.{next(count)}')

    shutil.copy(filename, backup)

    return backup


def find_project_root(
    start_dir: Path | str = '', markers: tuple[str, ...] | None = None
) -> Path:
    """Find the project root directory by looking for specific markers."""
    start_dir = Path(start_dir).expanduser().resolve()

    markers = markers or MARKERS[:]
    current = start_dir

    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent

    msg = 'Project root not found (no markers detected).'
    raise FileNotFoundError(msg)


def get_signed_off_by() -> str:
    """Obtém a linha de assinatura 'Signed-off-by' do committer atual.

    Usa `git var GIT_COMMITTER_IDENT` para extrair o nome e email do committer.

    Returns:
        str: Linha formatada no padrão:
             "Signed-off-by: Nome <email>"

    Raises:
        RuntimeError: Se a execução do comando git falhar.

    """
    try:
        ident: str = subprocess.check_output(
            ['git', 'var', 'GIT_COMMITTER_IDENT'], text=True
        ).strip()
    except (
        subprocess.CalledProcessError
    ) as e:  # pragma: no cover; noqa: S110 TODO cover in future
        msg = 'Falha ao obter GIT_COMMITTER_IDENT'
        raise RuntimeError(msg) from e

    return f'Signed-off-by: {ident.split(">", maxsplit=1)[0]}>'
