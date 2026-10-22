"""Precision."""

from decimal import Decimal, getcontext


def example():
    """Example."""
    # Set precision to 50 digits
    getcontext().prec = 50

    # Exact arithmetic
    a = Decimal('0.1')
    b = Decimal('0.2')
    print(a + b)  # Output: Decimal('0.3')

    # Rounding
    x = Decimal('2.56789')
    rounded = x.quantize(Decimal('0.01'), rounding='ROUND_HALF_UP')
    print(rounded)  # Output: Decimal('2.57')


if __name__ == '__main__':
    example()
