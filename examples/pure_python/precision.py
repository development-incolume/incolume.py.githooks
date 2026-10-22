"""Precision."""

from decimal import Decimal, getcontext

import icecream


def example() -> None:
    """Exampling."""
    # Set precision to 50 digits
    getcontext().prec = 50

    # Exact arithmetic
    a = Decimal('0.1')
    b = Decimal('0.2')
    icecream.ic(a + b)  # Output: Decimal('0.3')

    # Rounding
    x = Decimal('2.56789')
    rounded = x.quantize(Decimal('0.01'), rounding='ROUND_HALF_UP')
    icecream.ic(rounded)  # Output: Decimal('2.57')


if __name__ == '__main__':
    example()
