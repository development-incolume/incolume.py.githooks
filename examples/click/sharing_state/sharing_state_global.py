"""Source - https://stackoverflow.com/a/64729607.

Posted by dthor
Retrieved 2026-10-22, License - CC BY-SA 4.0
test1.py.
"""

import sys

import click
from icecream import ic


@click.pass_context
def some_func(ctx: click.Context, bar: callable) -> None:
    """Funct."""
    ic(f'{ctx.params=}\n {bar=}')
    foo = ctx.params['foo']
    ic(f'The value of foo is: {foo}')


@click.command()
@click.option('--foo')
@click.option('--bar')
def main(foo: str, bar: str) -> None:
    """Maint."""
    ic(f'{foo=}\n{bar=}')
    some_func(bar)


if __name__ == '__main__':
    # python test1.py --foo 1 --bar "bbb"
    sys.exit(main(sys.argv[1:]))
