"""Module to validate branch name."""
# ruff: noqa: E501

from __future__ import annotations

import re

import rich
from icecream import ic

from incolume.py.githooks.rules import (
    FAILURE,
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

    def __is_branch_dev(self, branchname: str = '') -> bool:
        """Check if the branch name is a default branch."""
        branchname = branchname or self.branchname
        result = branchname == ProtectedBranchName.DEV.value
        if result:
            self.violation_text = (
                f'\n - Branch name "{branchname}" is protected.'
            )
        return result

    def __is_branch_tags(self, branchname: str = '') -> bool:
        """Check if the branch name is a default branch."""
        branchname = branchname or self.branchname
        result = branchname == ProtectedBranchName.TAGS.value
        if result:
            self.violation_text = (
                f'\n - Branch name "{branchname}" is protected.'
            )
        return result

    def __is_branch_main(self, branchname: str = '') -> bool:
        """Check if the branch name is main branch."""
        branchname = branchname or self.branchname
        result = branchname in {
            ProtectedBranchName.MAIN.value,
            ProtectedBranchName.MASTER.value,
        }
        if result:
            self.violation_text = (
                f'\n - Branch name "{branchname}" is protected.'
            )
        return result

    def __is_refused(self, branchname: str = '') -> bool:
        """Check if the branch name is refused."""
        branchname = branchname or self.branchname
        r = re.match(RULE_BRANCHNAME_REFUSED, branchname, flags=re.IGNORECASE)
        if result := bool(r):
            self.violation_text = '\n - Can not be WIP (Work in Progress)'
        return result

    def __is_github_branch(self, branchname: str = '') -> bool:
        """Check if the branchname is a GitHub rule."""
        branchname = branchname or self.branchname

    def __is_not_matches_rule(self, branchname: str = '') -> bool:
        """Check if the branch name matches the rule."""
        branchname = branchname or self.branchname
        if not bool(re.match(RULE_BRANCHNAME, branchname)):
            self.violation_text = (
                "\n - Syntaxe 1: 'enhancement-<epoch-timestamp>'; or"
                "\n - Syntaxe 2: '<issue-id>-descrição-da-issue'; or"
                "\n - Syntaxe 3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or"
                "\n - Syntaxe 4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'"
            )
            return True
        return False

    def is_valid(self, **kwargs: str) -> int:
        """Validate branch name.

        Args:
          kwargs:
            branchname (str, Active branch): Branch name to validate.
            protected_dev (bool, False): Consider dev as protected branch.
            protected_tags (bool, False): Consider tags as protected branch.
            protected_main (bool, True): Consider main/master as protected branch.

        Returns:
            int: Status code.

        """
        branchname = kwargs.get('branchname') or self.branchname
        protected_dev = kwargs.get('protected_dev', False)
        protected_tags = kwargs.get('protected_tags', False)
        protected_main = kwargs.get('protected_main', True)

        ic(branchname)
        ic(self.result)
        msg: str = ''

        if protected_main and self.__is_branch_main(branchname):
            ic('is main protected branches')
            self.result.code = FAILURE
            msg += self.violation_text

        if protected_dev and self.__is_branch_dev(branchname):
            ic('is dev protected branches')
            self.result.code = FAILURE
            msg += self.violation_text

        if protected_tags and self.__is_branch_tags(branchname):
            ic('is tags protected branches')
            self.result.code = FAILURE
            msg += self.violation_text

        if self.__is_refused(branchname):
            ic('is refused branch')
            self.result.code = FAILURE
            msg += self.violation_text

        if self.__is_not_matches_rule(branchname):
            ic('is not matches rule')
            self.result.code = FAILURE
            msg += self.violation_text

        if self.result.code == FAILURE:
            rich.print(self.msg_refused.format(msg))
        else:
            rich.print(self.msg_ok)
        return self.result.code.value


if __name__ == '__main__':
    v = ValidateBranchname()
    v.is_valid()
