"""Verify if pre-commit is installed."""
# ruff: noqa: E501 T201

from pathlib import Path

from colorama import Fore, Style


def run() -> int:
    """Run it."""
    if not Path('.pre-commit-config.yaml').exists():
        print(
            f'{Fore.RED}pre-commit configuration detected, but `pre-commit install` was never run{Style.RESET_ALL}',
        )
        return 1
    return 0


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())
