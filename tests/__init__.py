"""Module tests."""

from os import getenv

from icecream import ic

DEBUG_MODE = getenv('DEBUG_MODE') or getenv('INCOLUME_DEBUG_MODE') or False
ic.disable()  # Disable by default

if DEBUG_MODE:
    ic.enable()
