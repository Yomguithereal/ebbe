# =============================================================================
# Ebbe Functions Unit Tests
# =============================================================================
from ebbe import with_prev


class TestFunctions(object):
    def test_with_prev(self):
        a = [1, 2, 3, 4]

        result = list(with_prev(a))

        assert result == [(1, 2), (2, 3), (3, 4)]
