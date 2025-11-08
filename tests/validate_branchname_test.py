"""Test for module validate_branchname."""

# ruff: noqa: SLF001

import pytest
from incolume.py.githooks.validate_branchname import ValidateBranchname


class TestCaseValidateBranchname:
    """Test class for ValidateBranchname."""

    def test_asdict(self) -> None:
        """Test asdict method."""
        v = ValidateBranchname()
        result = v.asdict()
        assert isinstance(result, dict)
        assert 'msg_ok' in result
        assert 'msg_refused' in result
        assert 'violation_text' in result
        assert 'result' in result
        assert 'branchname' in result

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('main', False, marks=[]),
            pytest.param('develop', False, marks=[]),
            pytest.param('feature/epoch#1234567890', False, marks=[]),
            pytest.param('123-jesus-loves-you', False, marks=[]),
            pytest.param('wip-fix-bug', False, marks=[]),
            pytest.param('dev', True, marks=[]),
            pytest.param('tags', False, marks=[]),
        ],
    )
    def test_is_dev_branch(self, *, branchname: str, expected: bool) -> None:
        """Test is_default_branch method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_branch_dev(branchname) == expected

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('main', False, marks=[]),
            pytest.param('develop', False, marks=[]),
            pytest.param('feature/epoch#1234567890', False, marks=[]),
            pytest.param('123-jesus-loves-you', False, marks=[]),
            pytest.param('wip-fix-bug', False, marks=[]),
            pytest.param('dev', False, marks=[]),
            pytest.param('tags', True, marks=[]),
        ],
    )
    def test_is_tags_branch(self, *, branchname: str, expected: bool) -> None:
        """Test is_default_branch method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_branch_tags(branchname) == expected

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('main', True, marks=[]),
            pytest.param('master', True, marks=[]),
            pytest.param('develop', False, marks=[]),
            pytest.param('feature/epoch#1234567890', False, marks=[]),
            pytest.param('123-jesus-loves-you', False, marks=[]),
            pytest.param('wip-fix-bug', False, marks=[]),
            pytest.param('dev', False, marks=[]),
            pytest.param('tags', False, marks=[]),
        ],
    )
    def test_is_main_branch(self, *, branchname: str, expected: bool) -> None:
        """Test is_default_branch method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_branch_main(branchname) == expected

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
        assert v._ValidateBranchname__is_branch_main(branchname) is expected

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
    def test_is_not_matches_rule(
        self, *, branchname: str, expected: bool
    ) -> None:
        """Test matches_rule method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_not_matches_rule(branchname) == expected
        )

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('123-abc', True, marks=[]),
            pytest.param('1-jesus-te-ama', True, marks=[]),
            pytest.param('WIP', False, marks=[]),
            pytest.param('123abcd', False, marks=[]),
            pytest.param('1-ab', False, marks=[]),
            pytest.param('feature/issue#123', False, marks=[]),
            pytest.param('enhancement-1627890123', False, marks=[]),
        ],
    )
    def test_is_github_branch(self, branchname, expected) -> None:
        """Test is_github_branch method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_github_branch(branchname) is expected

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('123-abc', False, marks=[]),
            pytest.param('1-jesus-te-ama', False, marks=[]),
            pytest.param('WIP', False, marks=[]),
            pytest.param('123abcd', False, marks=[]),
            pytest.param('1-ab', False, marks=[]),
            pytest.param('feature/issue#123', False, marks=[]),
            pytest.param('enhancement-1627890123', True, marks=[]),
        ],
    )
    def test_is_enhancement_epoch(self, branchname, expected) -> None:
        """Test is_github_branch method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_enhancement_epoch(branchname) is expected
        )

    @pytest.mark.parametrize(
        ['branchname', 'expected'],
        [
            pytest.param('123-abc', False, marks=[]),
            pytest.param('1-jesus-te-ama', False, marks=[]),
            pytest.param('WIP', False, marks=[]),
            pytest.param('123abcd', False, marks=[]),
            pytest.param('1-ab', False, marks=[]),
            pytest.param('feat/issue#123', True, marks=[]),
            pytest.param('fix/epoch#123', True, marks=[]),
            pytest.param('enhancement-1627890123', False, marks=[]),
        ],
    )
    def test_is_incolume_branch_rule(self, branchname, expected) -> None:
        """Test is_github_branch method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_incolume_branch_rule(branchname)
            is expected
        )
