"""Shout example."""

import sys

import click

from incolume.py.githooks.core import (
    CONTEXT_SETTINGS_CLICK,
    __package_name__,
    __version__,
)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='shoutter',
)
@click.option(
    '--shout/--no-shout', '-S', default=False, help='Toggle shouting mode.'
)
@click.argument('text', type=str)
def shoutter(text: str, *, shout: bool) -> None:
    """Shout text."""
    click.echo(text.upper() if shout else text.casefold())


if __name__ == '__main__':
    sys.exit(shoutter(sys.argv[1:]))
