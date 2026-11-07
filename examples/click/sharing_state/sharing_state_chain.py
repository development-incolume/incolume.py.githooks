"""Initialize the group with a context object."""

import sys

import click


@click.group(chain=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Ensure ctx.obj is a dictionary to store shared state."""
    ctx.ensure_object(dict)
    ctx.obj['status'] = 'initialized'


@cli.command()
@click.pass_context
def update(ctx: click.Context) -> None:
    """Update the context object."""
    ctx.obj['status'] = 'updated'
    click.echo(f'Status updated to: {ctx.obj["status"]}')


@cli.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """Read the updated context."""
    click.echo(f'Current status: {ctx.obj["status"]}')


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
