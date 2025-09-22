"""Module utils for project."""

from os import getenv

from icecream import ic


def debug_enable() -> bool:
    """Enable debug mode."""
    valid: list = ['1', 'True', 'true']
    debug: str = (
        getenv('DEBUG') in valid
        or getenv('DEBUG_MODE') in valid
        or getenv('INCOLUME_DEBUG_MODE') in valid
        or False
    )

    ic.disable()  # Disable by default

    if debug:
        ic.enable()

    return debug
