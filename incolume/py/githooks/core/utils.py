"""Module core.utils."""

from pathlib import Path
from typing import Final

MARKERS: Final[tuple[str, ...]] = (
    'pyproject.toml',
    '.git',
    'requirements.txt',
    'setup.cfg',
    '.venv',
)


def find_project_root(
    start_dir: Path | str = '', markers: tuple[str, ...] | None = None
) -> Path:
    """Find the project root directory by looking for specific markers."""
    if isinstance(start_dir, str):
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
