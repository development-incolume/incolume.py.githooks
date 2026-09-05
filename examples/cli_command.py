"""Module for hook to run CLI commands."""

from __future__ import annotations

import json
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys

PASS = 0
FAIL = 1


def main() -> int:
    """Execute a list of commands using the Hamilton CLI."""
    commands = sys.argv[1:]

    if len(commands) == 0:
        return PASS

    exit_code = PASS
    for command in commands:
        try:
            args = command.split(' ')
            # insert `--json-out` right after
            # `hamilton` for proper stdout parsing
            # no issue if `--json-out` is present twice
            args.insert(1, '--json-out')
            result = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
                args, check=False, stdout=subprocess.PIPE, text=True
            )
            response = json.loads(result.stdout)

            if response['success'] is False:
                raise ValueError  # ruff: ignore[raise-within-try]

        except Exception:  # ruff: ignore[blind-except, try-except-in-loop]
            exit_code |= FAIL

    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
