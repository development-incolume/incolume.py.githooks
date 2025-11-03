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
    def test_is_branch_main(self, branchname, expected) -> None:
        """Test is_branch_main method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_branch_main(branchname)
            is expected
        )

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            ('feature/issue#123', False),
            ('feat/epoch#1627890123', False),
            ('bugfix/issue#456', False),
            ('fix/epoch#1627890123', False),
            ('refactor/epoch#1627890123', False),
            ('enhancement-1627890123', False),
            ('789-new-feature', False),
            ('main', True),
            ('WIP', True),
            ('random-branch-name', True),
            ('feature/invalid#name', True),
            ('123', True),
        ],
    )
    def test_is_not_matches_rule(self, *, branchname: str, expected: bool) -> None:
        """Test matches_rule method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_not_matches_rule(branchname) == expected
