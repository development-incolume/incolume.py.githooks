"""Decorators module for githooks utilities.

Módulo que expõe decoradores de função (my_decorator, simple_decorator,
critical_log_call, logging_call) usados pelos hooks do projeto.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar, cast

from deprecated import deprecated
from icecream import ic

from incolume.py.githooks.core import debug_var_active
from incolume.py.githooks.core.rules import LoggingLevel

P = ParamSpec('P')
R = TypeVar('R')
F = TypeVar('F', bound=Callable[..., Any])


def my_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """Decora uma função para adicionar log antes e depois da chamada.

    Args:
        func: Função a ser decorada.

    Returns:
        Uma função wrapper que loga a chamada e invoca `func`.

    Example:
        >>> @my_decorator
        ... def soma(x: int, y: int) -> int:
        ...     return x + y
        >>> soma(1, 2)
        3

    """

    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        """Loga a chamada e invoca `func` antes e depois."""
        ic(f'Before function "{func.__name__}" call')
        result = func(*args, **kwargs)
        ic(f'After function "{func.__name__}" call')
        return result

    return wrapper


def simple_decorator(func: F) -> F:
    """Decora uma função para adicionar log antes e depois da chamada.

    Args:
        func: Função a ser decorada.

    Returns:
        Uma função wrapper que loga a chamada e invoca `func`.

    Example:
        >>> @simple_decorator
        ... def soma(x: int, y: int) -> int:
        ...     return x + y
        >>> soma(1, 2)
        3

    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # ruff: ignore[any-type]
        """Loga a chamada e invoca `func` antes e depois."""
        ic(f'Before function "{func.__name__}" call')
        result = func(*args, **kwargs)
        ic(f'After function "{func.__name__}" call')
        return result

    return cast('F', wrapper)


@deprecated(version='1.10.0', reason='Deprecated in favor of `logging_call`.')
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
    """Decora uma função para adicionar registros de logging.

    Args:
        level: Nível de logging, padrão é DEBUG.
        message: Modelo de mensagem de logging, padrão é mensagem genérica.

    Returns:
        Um decorador que adiciona logging à função decorada.

    Example:
        >>> @logging_call()
        ... @my_decorator
        ... def func() -> None:
        ...     pass
        >>> func()

    """
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
                executable = (
                    f'Calling function: {func.__name__},',
                    f' Arguments: {args}, {kwargs}',
                )
                ic(executable)

            result = func(*args, **kwargs)

            getattr(logging, level.name.casefold())(
                message.format(func.__name__)
            )
            return result

        return wrapper

    return inner


if __name__ == '__main__':

    @my_decorator
    def add_numbers(x: int, y: int) -> int:
        """Add numbers."""
        return x + y

    @simple_decorator
    def sum_numbers(x: int, y: int) -> int:
        """Sum numbers."""
        return x + y

    add_numbers(1, 2)
    sum_numbers(1, 2)
