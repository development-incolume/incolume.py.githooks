"""Module to validate branch name."""

from __future__ import annotations

import re

import rich
from icecream import ic

from incolume.py.githooks.rules import (
    RULE_BRANCHNAME,
    RULE_BRANCHNAME_REFUSED,
    ProtectedBranchName,
)
from incolume.py.githooks.utils import Result, debug_enable, get_branchname

debug_enable()


class ValidateBranchname:
    """Rules for valid branch name."""

    def __init__(self) -> None:
        """Init."""
        self.msg_ok = '[green]Branching name rules. [OK][/green]'
        self.msg_refused = (
            '[red]Your commit was rejected due to branching name '
            'incompatible with rules.'
            '{}[/red]'
        )
        self.violation_text = ''
        self.result: Result = Result()
        self.branchname = get_branchname()

    def is_default_branch(self, branchname: str = '') -> bool:
        """Check if the branch name is a default branch."""
        branchname = branchname or self.branchname
        return branchname in ProtectedBranchName.to_list()

    def is_refused(self, branchname: str) -> bool:
        """Check if the branch name is refused."""
        r = re.match(RULE_BRANCHNAME_REFUSED, branchname, flags=re.IGNORECASE)
        if bool(r):
            self.violation_text = '\n - Can be not WIP(Work in Progress)'
            return True
        return False

    def is_github_branch(self, branchname: str = '') -> bool:
        """Check if the branchname is a GitHub rule."""

    def matches_rule(self, branchname: str = '') -> bool:
        """Check if the branch name matches the rule."""
        branchname = branchname or self.branchname
        if not bool(re.match(RULE_BRANCHNAME, branchname)):
            self.violation_text = (
                "\n- syntaxe 1: 'enhancement-<epoch-timestamp>'"
                "\n- syntaxe 2: '<issue-id>-descrição-da-issue'"
                "\n- syntaxe 3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'"
                "\n- syntaxe 4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'"  # noqa: E501
            )
            return True
        return False

    def is_valid(self) -> int:
        """Validate branch name."""
        ic(self.branchname)
        ic(self.result)

        # if self.is_default_branch(self.branchname):
        #     self.result.code = FAILURE

        if self.is_refused(self.branchname):
            self.result.message += self.violation_text
            # self.result.code = FAILURE

        # if self.matches_rule(self.branchname) is False:
        #     self.result.message += self.violation_text
        #     self.result.code = FAILURE

        rich.print(self.msg_refused.format(self.violation_text))
        return 1
