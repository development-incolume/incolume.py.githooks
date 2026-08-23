"""Decorators module for githooks utilities."""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

from deprecated import deprecated
from icecream import ic

from incolume.py.githooks.core import debug_enable, debug_var_active
from incolume.py.githooks.core.rules import LoggingLevel

P = ParamSpec('P')
R = TypeVar('R')

debug_enable()


def my_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Model decorator."""

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        ic(f'Before function "{func.__name__}" call')
        result = func(*args, **kwargs)
        ic(f'After function "{func.__name__}" call')
        return result

    return wrapper


@deprecated(version='1.10.0', reason='Deprecated in favor of `logging_call`.')  # type: ignore[untyped-decorator]
def critical_log_call(func: Callable[P, R]) -> Callable[P, R]:
    """Decoratore to debug function calls."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
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
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decoratore to debug function calls.

    Args:
      level::str: Level logging, default is debug;
      message::str: Message logging, default is ;

    """
    match level:
        case _:
            level = LoggingLevel(level)

    message = message or 'Function **{}** called.'

    def inner(func: Callable[P, R]) -> Callable[P, R]:
        """Inner funtion to receive parameters."""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrapp function to add logging record."""
            debug: bool = debug_var_active()

            if debug:
                ic.enable()
                m1 = (
                    f'Calling function: {func.__name__},',
                    f' Arguments: {args}, {kwargs}',
                )
                ic(m1)

            result = func(*args, **kwargs)

            getattr(logging, level.name.casefold())(
                ic(message.format(func.__name__))
            )
            return result

        return wrapper

    return inner


if __name__ == '__main__':

    @my_decorator
    def add_numbers(x: int, y: int) -> int:
        """Add numbers."""
        return x + y

    add_numbers(1, 2)
