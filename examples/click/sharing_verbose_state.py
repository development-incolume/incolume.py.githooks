"""Example of sharing verbose state.

Sharing verbose state between commands using Click's context object.
"""

import sys

import click

from incolume.py.githooks.core import (
    CONTEXT_SETTINGS_CLICK,
    __package_name__,
    __version__,
)


@click.group(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='shoutter',
)
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx: click.Context, *, verbose: bool) -> None:
    """Maint entry point for the CLI."""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose  # Store in context


@cli.command()
@click.pass_context
def subcommand(ctx: click.Context) -> None:
    """Run A subcommand that uses the verbose state."""
    if ctx.obj['verbose']:
        click.secho('Verbose mode active', fg='yellow')
    click.secho('Running subcommand...', fg='cyan')


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
