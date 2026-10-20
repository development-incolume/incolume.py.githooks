"""Method 2: Using ctx.params for Direct Access.

Access command-line arguments directly from the context's params dictionary.
"""

import sys
from collections.abc import Mapping
from typing import Any

import click
from icecream import ic


@click.command()
@click.option('--name', default='World', required=False, help='Name to greet')
@click.pass_context
def hello(ctx: click.Context, **kwarg: Mapping[str, Any]) -> None:
    """Access option value via context."""
    ic(kwarg)
    name = ctx.params[
        'name'
    ].capitalize()  # Accessing the option value directly from ctx.params
    click.echo(f'Hello, {name}!')


if __name__ == '__main__':
    sys.exit(hello(sys.argv[1:]))
