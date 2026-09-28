"""Example.

adaptado e acessado em 2026-09-22 as 12h16 disponível em:
https://search.brave.com/search?q=python+click+argument+optional+example&conversation=0998c8373f9d05cdee78ee04e6c8efba760b
"""

import sys
from pathlib import Path

import click


@click.command()
@click.argument('filename', required=False)
def process(filename: Path) -> None:
    """Process document fake.

    example for optional document.
    """
    if filename:
        click.secho(f'Processing file: {filename}', fg='green')
    else:
        click.secho('No file specified.')


if __name__ == '__main__':
    sys.exit(process(sys.argv[1:]))
