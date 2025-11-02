"""Module to validate branch name."""

from __future__ import annotations

import re

import rich
from icecream import ic

from incolume.py.githooks.rules import (
    FAILURE,
    RULE_BRANCHNAME,
    RULE_BRANCHNAME_NOT_REFUSED,
    SUCCESS,
    ProtectedBranchName,
)
from incolume.py.githooks.utils import get_branchname


class ValidateBranchname:
    """Rules for valid branch name."""

    msg_ok = '[green]Branching name rules. [OK][/green]'
    msg_refused = (
        '[red]Your commit was rejected due to branching name '
        'incompatible with rules.'
        '{}[/red]'
    )
    violation_text = ''

    status = SUCCESS
    branchname = get_branchname()

    def is_default_branch(self, branchname: str) -> bool:
        """Check if the branch name is a default branch."""
        if branchname in ProtectedBranchName.to_list():
            rich.print(self.msg_ok)
            return True
        return False

    def is_refused(self, branchname: str) -> bool:
        """Check if the branch name is refused."""
        if re.match(
            RULE_BRANCHNAME_NOT_REFUSED, branchname, flags=re.IGNORECASE
        ):
            rich.print(
                self.msg_refused.format(
                    '\n - Can be not WIP(Work in Progress)'
                )
            )
            return True
        return False

    def matches_rule(self, branchname: str = '') -> int:
        """Check if the branch name matches the rule."""
        branchname = branchname or self.branchname
        if not re.match(RULE_BRANCHNAME, branchname):
            result = (
                '[red]Your commit was rejected due to branching name '
                'incompatible with rules.\n'
                'Please rename your branch with:'
                "\n- syntaxe 1: 'enhancement-<epoch-timestamp>'"
                "\n- syntaxe 2: '<issue-id>-descrição-da-issue'"
                "\n- syntaxe 3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'"
                "\n- syntaxe 4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'"  # noqa: E501
                '[/red]'
            )
            status |= FAILURE

    def is_valid(self) -> int:
        """Validate branch name."""
        ic(self.branchname)
        rich.print(self.msg_ok)
        return SUCCESS.value
