"""A função chain do módulo itertools combina múltiplos iteráveis.

Torna multiplos iteráveis em um único iterador, processando-os
sequencialmente de forma eficiente em memória (lazy evaluation).
"""

from collections.abc import Sequence
from itertools import chain

from icecream import ic


def run() -> None:
    """Run it."""
    a, b = [1, 2], ['a', 'b']  # [1, 2, 'a', 'b']
    c = [a, b]  # [1, 2, 'a', 'b']
    entrance = a, b

    ic(
        list(chain(*entrance)),
        list(chain.from_iterable(c)),
    )


if __name__ == '__main__':
    run()
