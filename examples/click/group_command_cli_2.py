"""Example."""

import sys

import click

from incolume.py.githooks.core import CONTEXT_SETTINGS_CLICK


@click.group(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.pass_context
def cli(ctx: click.Context) -> click.Context:
    """Command Line Interface."""


@cli.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.pass_context
@click.option(
    '--success/--failure',
    '-s/-f',
    'success',
    default=False,
    help='Success or Failure.',
)
def task0(ctx: click.Context, *, success: bool) -> click.Context:
    """Perform task logic."""
    if not success:
        # Exit with code 1 and trigger cleanup
        ctx.exit(1)

    # Exit with code 0 on success
    ctx.exit(0)


@cli.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.pass_context
@click.option(
    '--success/--failure',
    '-s/-f',
    'success',
    default=False,
    help='Success or Failure.',
)
def task1(ctx: click.Context, *, success: bool) -> click.Context:
    """Perform task logic."""
    if not success:
        # Exit with code 1 and trigger cleanup
        ctx.exit(1)

    # Exit with code 0 on success
    ctx.exit(0)


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
