"""Source - https://stackoverflow.com/a/70549636.

Posted by haridsv, modified by community.
See post 'Timeline' for change history
Retrieved 2026-10-22, License - CC BY-SA 4.0
"""

import functools
import sys

import click
from icecream import ic


def with_click_params(func: callable) -> callable:
    """With click params."""

    @functools.wraps(func)
    def wrapper(*args: str, **kwargs: str) -> callable:
        """Run wrapper function."""
        g = func.__globals__
        sentinel = object()

        ctx = click.get_current_context()
        oldvalues = {}
        for param in ctx.params:
            oldvalues[param] = g.get(param, sentinel)
            g[param] = ctx.params[param]

        try:
            return func(*args, **kwargs)
        finally:
            for param in ctx.params:
                if oldvalues[param] is sentinel:
                    del g[param]
                else:
                    g[param] = oldvalues[param]

    return wrapper


@with_click_params
def some_func() -> None:
    """Run function."""
    ic(f'The value of foo is: {foo}')  # ruff: ignore[undefined-name]
    ic(f'The value of bar is: {bar}')  # ruff: ignore[undefined-name]


@click.command()
@click.option('--foo')
@click.option('--bar')
def main(foo: str, bar: str) -> None:
    """Maint."""
    ic(f'{foo=}, {bar=}')
    some_func()


if __name__ == '__main__':
    """
    $ python test2.py --foo 1 --bar "bbb"
    The value of foo is: 1
    The value of bar is: bbb
    """
    sys.exit(main(sys.argv[1:]))
