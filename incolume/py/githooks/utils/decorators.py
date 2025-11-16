"""Decorators module for githooks utilities."""

from __future__ import annotations

import logging
from functools import wraps
from pathlib import Path
from typing import TYPE_CHECKING

from icecream import ic

from . import debug_enable, debug_var_active

if TYPE_CHECKING:
    from collections.abc import Callable

debug_enable()



def critical_log_call(func: Callable) -> Callable:
    """Decoratore to debug function calls."""

    @wraps(func)
    def wrapper(*args: str, **kwargs: dict) -> None:
        """Wrapp function to add logging critical."""
        debug: bool = debug_var_active()

        if debug:
            ic.enable()
            ic(f'Calling function: {func.__name__}')
            ic(f'Arguments: {args}, {kwargs}')

        result = func(*args, **kwargs)

        logging.critical(
            ic(f'Function **{func.__name__}** called with critial status.')
        )

        return result

    return wrapper
