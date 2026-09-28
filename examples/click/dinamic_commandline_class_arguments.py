"""Example from https://www.zonca.dev/posts/2022-10-26-click-commandline-class-arguments."""

import inspect
import logging
import sys
from collections.abc import Callable

import click

from incolume.py.githooks.core import CONTEXT_SETTINGS_CLICK


class AClass:
    """Class A."""

    def __init__(self, a: str, b: int) -> None:
        """Init this."""


class BClass:
    """Class B."""

    def __init__(self, c: float, under_score: str, *, d: bool) -> None:
        """Init this."""


def options_from_class(cls: Callable) -> Callable:
    """Get options from class."""

    def decorator(f: Callable) -> Callable:
        """Set dinamics arguments."""
        for par in inspect.signature(cls.__init__).parameters.values():
            if par.name != 'self':
                click.option(
                    '--' + par.name, required=True, type=par.annotation
                )(f)
        return f

    return decorator


@click.group(context_settings=CONTEXT_SETTINGS_CLICK)
def cli() -> None:
    """Command Line Interface."""


@cli.command()
@options_from_class(AClass)
def aclass(**kwargs: str) -> None:
    """Command newer."""
    click.echo(f'kwargs: {kwargs}')
    ac = AClass(**kwargs)
    logging.debug(ac)


@cli.command()
@options_from_class(BClass)
def bclass(**kwargs: str) -> None:
    """Command newer."""
    click.echo(f'kwargs: {kwargs}')
    bc = BClass(**kwargs)
    logging.debug(bc)


if __name__ == '__main__':
    sys.exit(cli(sys.argv[:1]))
