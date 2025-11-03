"""Test for module validate_branchname."""

# ruff: noqa: SLF001

import pytest
from incolume.py.githooks.validate_branchname import ValidateBranchname


class TestCaseValidateBranchname:
    """Test class for ValidateBranchname."""

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            ('main', True),
            ('develop', False),
            ('feature/epoch#1234567890', False),
            ('123-jesus-loves-you', False),
            ('wip-fix-bug', False),
            ('dev', True),
            ('tags', True),
        ],
    )
    def test_is_protected_branch(
        self, *, branchname: str, expected: bool
    ) -> None:
        """Test is_default_branch method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_protected_branch(branchname) == expected
        )

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            ('WIP', True),
            ('Wip', True),
            ('wip', True),
            ('wip-fix-bug', True),
            ('fix/issue#123', False),
            ('enhancement-1627890123', False),
        ],
    )
    def test_is_refused(self, *, branchname: str, expected: bool) -> None:
        """Test is_refused method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_refused(branchname) == expected

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('main', True, marks=[]),
            pytest.param('master', True, marks=[]),
            pytest.param('develop', False, marks=[]),
        ],
    )
    def test_is_branch_main_or_tags(self, branchname, expected) -> None:
        """Test is_branch_main method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_branch_main_or_tags(branchname)
            is expected
        )

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            ('feature/issue#123', True),
            ('feat/epoch#1627890123', True),
            ('bugfix/issue#456', True),
            ('fix/epoch#1627890123', True),
            ('refactor/epoch#1627890123', True),
            ('enhancement-1627890123', True),
            ('789-new-feature', True),
            ('main', False),
            ('WIP', False),
            ('random-branch-name', False),
            ('feature/invalid#name', False),
            ('123', False),
        ],
    )
    def test_is_matches_rule(self, *, branchname: str, expected: bool) -> None:
        """Test matches_rule method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_matches_rule(branchname) == expected
