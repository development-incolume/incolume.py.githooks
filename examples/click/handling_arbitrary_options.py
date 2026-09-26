"""Exemplo.

Manipulação de opçoes arbitrarias.
"""

import sys

import click
from icecream import ic

from incolume.py.githooks.core import CONTEXT_SETTINGS_CLICK


@click.command(
    context_settings={
        **CONTEXT_SETTINGS_CLICK,
        'ignore_unknown_options': True,
        'allow_extra_args': True,
    }
)
@click.pass_context
def cli(ctx: dict) -> None:
    """Principal CLI."""
    # Parse extra args into a dictionary
    # Assumes pairs like --key value
    kwargs = {}
    args = ctx.args
    ic(args)
    i = 0
    while i < len(args):
        key = args[i]
        ic(key)
        if key.startswith('--'):
            key = key[2:]  # Remove --
            if i + 1 < len(args) and not args[i + 1].startswith('--'):
                kwargs[key] = args[i + 1]
                i += 2
            else:
                kwargs[key] = True  # Boolean flag
                i += 1
        else:
            i += 1

    click.echo(f'Captured kwargs: {kwargs}')


if __name__ == '__main__':
    sys.exit(cli(sys.argv[:1]))
