"""# Source - https://stackoverflow.com/a/64729607
# Posted by dthor
# Retrieved 2026-10-22, License - CC BY-SA 4.0
# test1.py
"""

import click


@click.pass_context
def some_func(ctx, bar):
    foo = ctx.params['foo']
    print(f'The value of foo is: {foo}')


@click.command()
@click.option('--foo')
@click.option('--bar')
def main(foo, bar):
    some_func(bar)


if __name__ == '__main__':
    main()
