"""Example."""

import sys

import click

from incolume.py.githooks import __package_name__, __version__
from incolume.py.githooks.core.rules import CONTEXT_SETTINGS_CLICK


@click.group(
    'printer_group',
    no_args_is_help=True,
    context_settings=CONTEXT_SETTINGS_CLICK,
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='command-group',
)
def command_group() -> None:
    """Command group."""


@command_group.command('printer', context_settings=CONTEXT_SETTINGS_CLICK)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='printer',
)
@click.option('--this')
def printer(this: str) -> None:
    """Printer."""
    if this:
        click.echo(this)


@command_group.command(
    context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='printer',
)
@click.option('--this')
def show(this: str) -> None:
    """Show."""
    if this:
        click.secho(this, fg='blue')


@command_group.command(
    context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='printer',
)
@click.option('--this')
def display(this: str) -> None:
    """Display."""
    if this:
        click.secho(this, fg='yellow')


@command_group.command(
    context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True
)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='printer',
)
@click.option('--this')
def pprint(this: str) -> None:
    """Pprint."""
    if this:
        click.secho(this, fg='magenta')


if __name__ == '__main__':
    sys.exit(command_group(sys.argv[1:]))
