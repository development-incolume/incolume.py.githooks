"""Test for module validate_branchname."""

# ruff: noqa: E501 SLF001

import pytest
from incolume.py.githooks.rules import Status
from incolume.py.githooks.utils import Result
from incolume.py.githooks.validate_branchname import ValidateBranchname


class TestCaseValidateBranchname:
    """Test class for ValidateBranchname."""

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param('msg_ok', marks=[]),
            pytest.param('msg_refused', marks=[]),
            pytest.param('violation_text', marks=[]),
            pytest.param('result', marks=[]),
            pytest.param('branchname', marks=[]),
        ],
    )
    def test_asdict(self, entrance: str) -> None:
        """Test asdict method."""
        v = ValidateBranchname()
        result = v.asdict()
        assert isinstance(result, dict)
        assert entrance in result

    @pytest.mark.parametrize(
        ['branchname', 'violation_txt', 'expected'],
        [
            pytest.param('main', '', True, marks=[]),
        ],
    )
    def test_is_lenght_valid(
        self, *, branchname: str, violation_txt: str, expected: bool
    ) -> None:
        """Test if lenght branchname is valid."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_length_valid(branchname) == expected
        assert v.violation_text == violation_txt

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
        ['branchname', 'violation_txt', 'expected'],
        [
            ('WIP', '\n - Can not be WIP (Work in Progress)', True),
            ('Wip', '\n - Can not be WIP (Work in Progress)', True),
            ('wip', '\n - Can not be WIP (Work in Progress)', True),
            ('wip-fix-bug', '\n - Can not be WIP (Work in Progress)', True),
            ('fix/issue#123', '', False),
            ('enhancement-1627890123', '', False),
        ],
    )
    def test_is_refused(
        self, *, branchname: str, violation_txt: str, expected: bool
    ) -> None:
        """Test is_refused method."""
        v = ValidateBranchname()
        assert v._ValidateBranchname__is_refused(branchname) == expected
        assert v.violation_text == violation_txt

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
        ['branchname', 'violation_txt', 'expected'],
        [
            ('feature/issue#123', '', False),
            ('feat/epoch#1627890123', '', False),
            ('bugfix/issue#456', '', False),
            ('fix/epoch#1627890123', '', False),
            ('refactor/epoch#1627890123', '', False),
            ('enhancement-1627890123', '', False),
            ('789-new-feature', '', False),
            (
                'main',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
            (
                'WIP',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
            (
                'random-branch-name',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
            (
                'feature/invalid#name',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
            (
                '123',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
            (
                'abc',
                "\n\n:: Permitted syntaxes:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-descrição-da-issue'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                True,
            ),
        ],
    )
    def test_is_not_matches_rule(
        self, *, branchname: str, violation_txt: str, expected: bool
    ) -> None:
        """Test matches_rule method."""
        v = ValidateBranchname()
        assert (
            v._ValidateBranchname__is_not_matches_rule(branchname) == expected
        )
        assert v.violation_text == violation_txt

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

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                'wip',
                Result(
                    Status.FAILURE,
                    """Your commit was rejected due to branching name incompatible with rules.
 - Can not be WIP (Work in Progress)

:: Permitted syntaxes:
 - #1: 'enhancement-<epoch-timestamp>'; or
 - #2: '<issue-id>-descrição-da-issue'; or
 - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or
 - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'""",
                ),
                marks=[pytest.mark.skip],
            ),
        ],
    )
    def test_is_valid(self, entrance, expected, capsys) -> None:
        """Test validate method."""
        v = ValidateBranchname()
        captured = capsys.readouterr()
        result = v.is_valid(entrance)
        assert expected.code.value == result
        assert expected.message == captured.out.strip()
