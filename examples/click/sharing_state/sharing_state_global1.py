"""Source - https://stackoverflow.com/a/64729607.

Posted by dthor
Retrieved 2026-10-22, License - CC BY-SA 4.0

test2.py
"""

import sys

import click
from icecream import ic


def some_func(bar: str) -> None:
    """Somer func."""
    ic(f'{bar=}')
    c = click.get_current_context()
    foo = c.params['foo']
    ic(f'The value of foo is: {foo}')


@click.command()
@click.option('--foo')
@click.option('--bar')
def main(foo: str, bar: str) -> None:
    """Maint."""
    ic(f'{foo=}, {bar=}')
    some_func(bar)


if __name__ == '__main__':
    # python test2.py --foo 1 --bar "bbb"
    sys.exit(main(sys.argv[1:]))
