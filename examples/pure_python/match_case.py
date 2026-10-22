"""Example match case."""

import decimal
import math

import icecream


def example(value: float | str) -> str:
    """Match case type."""
    match value:
        case bool():
            return f'{value} is a boolean'
        case int():
            return f'{value} is an integer'
        case str():
            return f'{value} is a string'
        case float():
            return f'{value} is a float'
        case _:
            return f'{value} is unknown'


def run() -> None:
    """Run it."""
    values = [
        1,
        'hello',
        True,
        math.pi,
        complex(3, 2),
        decimal.Decimal('0.00000001'),
        math.e,
        math.nan,
        None,
    ]
    for value in values:
        icecream.ic(example(value))


if __name__ == '__main__':
    run()
