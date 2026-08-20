"""Decorators module for githooks utilities."""

from __future__ import annotations

import logging
from functools import wraps
from typing import TYPE_CHECKING, Any

from deprecated import deprecated
from icecream import ic

from incolume.py.githooks.core import debug_enable, debug_var_active
from incolume.py.githooks.core.rules import LoggingLevel

if TYPE_CHECKING:
    from collections.abc import Callable

debug_enable()


@deprecated(version='1.10.0', reason='Deprecated in favor of `logging_call`.')  # type: ignore[untyped-decorator]
def critical_log_call(func: Callable[[Any], Any]) -> Callable[[], Any]:
    """Decoratore to debug function calls."""

    @wraps(func)
    def wrapper(*args: str, **kwargs: str) -> Any:
        """Wrapp function to add logging critical."""
        debug: bool = debug_var_active()

        if debug:
            ic.enable()
            ic(f'Calling function: {func.__name__}')
            ic(f'Arguments: {args}, {kwargs}')

        result = func(*args, **kwargs)

        logging.critical(
            'Function **%s** called with critial status.', func.__name__
        )

        return result

    return wrapper


def logging_call(
    level: LoggingLevel = LoggingLevel.DEBUG, message: str = ''
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decoratore to debug function calls.

    Args:
      level::str: Level logging, default is debug;
      message::str: Message logging, default is ;

    """
    match level:
        case _:
            level = LoggingLevel(level)

    message = message or 'Function **{}** called.'

    def inner(func: Callable) -> Callable:  # type: ignore[type-arg]
        """Inner funtion to receive parameters."""

        @wraps(func)
        def wrapper(*args: str, **kwargs: str) -> Callable[[], Any]:
            """Wrapp function to add logging record."""
            debug: bool = debug_var_active()

            if debug:
                ic.enable()
                ic(f'Calling function: {func.__name__}')
                ic(f'Arguments: {args}, {kwargs}')

            result = func(*args, **kwargs)

            getattr(logging, level.name.casefold())(
                ic(message.format(func.__name__))
            )
            return result

        return wrapper

    return inner
