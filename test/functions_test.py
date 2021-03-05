# =============================================================================
# Ebbe Functions Unit Tests
# =============================================================================
from ebbe import (
    with_prev,
    with_next
)


class TestFunctions(object):
    def test_with_prev(self):
        a = [1, 2, 3, 4]

        result = list(with_prev(a))

        assert result == [(None, 1), (1, 2), (2, 3), (3, 4)]

        result = list(with_prev([1]))

        assert result == [(None, 1)]

        result = list(with_prev([]))

        assert result == []

    def test_with_next(self):
        a = [1, 2, 3, 4]

        result = list(with_next(a))

        assert result == [(1, 2), (2, 3), (3, 4), (4, None)]

        result = list(with_next([1]))

        assert result == [(1, None)]

        result = list(with_next([]))

        assert result == []
