"""Module to validate branch name."""
# ruff: noqa: E501

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

import rich
from icecream import ic
from rich.console import Console

from incolume.py.githooks.core import debug_enable, get_branchname
from incolume.py.githooks.core.rules import (
    FAILURE,
    RULE_BRANCHNAME,
    RULE_BRANCHNAME_REFUSED,
    ProtectedBranchName,
    Result,
    TypeCommit,
)

debug_enable()


@dataclass
class ValidateBranchname:
    """Rules for valid branch name."""

    msg_ok: str = '\n[green]Branching name rules. [OK][/green]'
    msg_refused: str = (
        '\n[red]Your commit was rejected due to branching name '
        'incompatible with rules.'
        '{}[/red]'
    )
    violation_text: str = ''
    result: Result = field(default_factory=Result)
    branchname: str = field(default_factory=get_branchname)

    def asdict(self) -> dict:
        """Self dict."""
        return self.__dict__

    def __is_length_valid(self, branchname: str = '') -> bool:
        """Check if the branch name length is valid."""
        branchname = branchname or self.branchname
        regex: str = r'^[\w\d_-]{3,255}$'
        result = re.match(regex, branchname)

        if result:
            return True

        self.violation_text = (
            f'\n - Branch name "{branchname}" length is invalid.'
            ' Min 3 and Max 255 characters.'
        )
        return bool(result)

    def __is_branch_dev(self, branchname: str = '') -> bool:
        """Check if the branch name is a default branch."""
        branchname = branchname or self.branchname
        result = branchname in {ProtectedBranchName.DEV.value, 'development'}
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
        regex: str = RULE_BRANCHNAME_REFUSED
        result = re.match(regex, branchname, flags=re.IGNORECASE)
        ic(result)
        if result:
            self.violation_text = '\n - Can not be WIP (Work in Progress)'
        return bool(result)

    def __is_github_branch(self, branchname: str = '') -> bool:
        """Check if the branchname is a GitHub rule."""
        branchname = branchname or self.branchname
        regex_github = r'^\d+(-[\w_]{3,})+'

        return bool(re.match(regex_github, branchname))

    def __is_enhancement_epoch(self, branchname: str = '') -> bool:
        """Check if the branchname is enhancement-<epoch-timestamp>."""
        branchname = branchname or self.branchname
        regex_enhancement = r'^enhancement-\d{1,11}$'

        return bool(re.match(regex_enhancement, branchname))

    def __is_incolume_branch_rule(self, branchname: str = '') -> bool:
        """Check if the branchname is incolume rule."""
        branchname = branchname or self.branchname
        regex_incolume = (
            rf'^({"|".join(TypeCommit.to_set())})/(epoch|issue)#([0-9]+)$'
        )

        return bool(re.match(regex_incolume, branchname))

    def __is_not_matches_rule(self, branchname: str = '') -> bool:
        """Check if the branch name matches the rule."""
        branchname = branchname or self.branchname
        if not bool(re.match(RULE_BRANCHNAME, branchname)):
            self.violation_text = (
                '\n\n:: These syntaxes are allowed for branchname:'
                "\n - #1: 'enhancement-<epoch-timestamp>'; or"
                "\n - #2: '<issue-id>-issue-description'; or"
                "\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or"
                "\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'"
            )
            return True
        return False

    def is_valid(self, branchname: str = '', **kwargs: str) -> int:
        """Validate branch name.

        Args:
          branchname (str, Active branch): Branch name to validate.

          kwargs:
            protected_dev (bool, False): Consider dev as protected branch.
            protected_tags (bool, False): Consider tags as protected branch.
            protected_main (bool, True): Consider main/master as protected branch.

        Returns:
            int: Status code.

        """
        branchname = branchname or kwargs.get('branchname') or self.branchname
        protected_dev = kwargs.get('protected_dev', False)
        protected_tags = kwargs.get('protected_tags', False)
        protected_main = kwargs.get('protected_main', True)

        console = Console()
        logging.debug('detected: %s', ic(branchname))

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
            console.print(self.msg_ok)
        return self.result.code.value


if __name__ == '__main__':
    v = ValidateBranchname()
    v.is_valid()
