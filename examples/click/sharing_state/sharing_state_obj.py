"""Method 1: Using ctx.obj for Shared State.

Store shared configuration in the context object at the group level
and retrieve it in subcommands.
"""

import sys

import click


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx: click.Context, *, debug: bool) -> None:
    """Store shared options in the context object."""
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
def sync(ctx: click.Context) -> None:
    """Access the stored option."""
    if ctx.obj['DEBUG']:
        click.echo('Debug mode is on')
    click.echo('Syncing data...')


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
