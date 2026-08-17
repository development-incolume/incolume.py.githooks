"""Module core for project."""

from incolume.py.githooks.core.__main__ import (
    __version__,
    debug_enable,
    debug_var_active,
    get_branchname,
    get_git_diff,
    get_signed_off_by,
)

__all__ = [
    '__version__',
    'debug_enable',
    'debug_var_active',
    'get_branchname',
    'get_git_diff',
    'get_signed_off_by',
]
