"""Module core for project."""

from incolume.py.githooks.core.__main__ import (
    __package_name__,
    __version__,
    debug_enable,
    debug_var_active,
    get_commit_hash,
    get_git_diff,
    get_issue_from_branch,
    subprocess,
)
from incolume.py.githooks.core.rules import CONTEXT_SETTINGS_CLICK
from incolume.py.githooks.core.utils import (
    backup_file,
    get_branchname,
    get_signed_off_by,
    remove_color_tags,
)

__all__ = [
    'CONTEXT_SETTINGS_CLICK',
    '__package_name__',
    '__version__',
    'backup_file',
    'debug_enable',
    'debug_var_active',
    'get_branchname',
    'get_commit_hash',
    'get_git_diff',
    'get_issue_from_branch',
    'get_signed_off_by',
    'remove_color_tags',
    'subprocess',
]
