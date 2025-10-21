"""Test for rules module."""

import pytest
import incolume.py.githooks.rules as pkg


class TestCaseRules:
    """Test case rules."""

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(0),
            pytest.param(1),
        ],
    )
    def test_status_value(self, entrance) -> None:
        """Test status enum."""
        assert pkg.Status(entrance).value == entrance

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('success', 0),
            pytest.param('failure', 1),
            pytest.param(0, 0),
            pytest.param(1, 1),
            pytest.param('SUCCESS', 0),
            pytest.param('FAILURE', 1),
        ],
    )
    def test_status_enum(self, entrance, expected) -> None:
        """Test status enum."""
        assert pkg.Status(entrance).value == expected

    @pytest.mark.parametrize(
        ['ent0', 'ent1', 'expected'],
        [
            pytest.param(pkg.Status(0), pkg.Status(0), pkg.Status(0)),
            pytest.param(pkg.Status(0), pkg.Status(1), pkg.Status(1)),
            pytest.param(pkg.Status(1), pkg.Status(0), pkg.Status(1)),
            pytest.param(pkg.Status(1), pkg.Status(1), pkg.Status(1)),
            pytest.param(pkg.Status(0), 0, pkg.Status(0)),
            pytest.param(pkg.Status(0), 1, pkg.Status(1)),
            pytest.param(0, pkg.Status(0), pkg.Status(0)),
            pytest.param(1, pkg.Status(0), pkg.Status(1)),
        ],
    )
    def test_status_op(self, ent0, ent1, expected) -> None:
        """Status operations."""
        assert ent0 | ent1 == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                '0',
                {
                    'expected_exception': ValueError,
                    'match': "'0' is not a valid Status",
                },
            ),
            pytest.param(
                'fail',
                {
                    'expected_exception': ValueError,
                    'match': "'fail' is not a valid Status",
                },
            ),
            pytest.param('failure', {}),
        ],
    )
    def test_status_missing(self, entrance, expected) -> None:
        """Status missing."""
        try:
            with pytest.raises(**expected):  # noqa: PT010
                assert pkg.Status(entrance)
        except ValueError:
            assert pkg.Status(entrance)
