"""Example."""

import sys

import click


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> click.Context:
    """Command Line Interface."""


@cli.command()
@click.pass_context
def run_task(ctx: click.Context) -> click.Context:
    """Perform task logic."""
    success = False

    if not success:
        # Exit with code 1 and trigger cleanup
        ctx.exit(1)

    # Exit with code 0 on success
    ctx.exit(0)


if __name__ == '__main__':
    sys.exit(cli(sys.argv[1:]))
