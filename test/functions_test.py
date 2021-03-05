# =============================================================================
# Ebbe Functions Unit Tests
# =============================================================================
from ebbe import (
    as_chunks,
    uniq,
    with_prev,
    with_next,
    with_is_first,
    with_is_last
)


class TestFunctions(object):
    def test_as_chunks(self):
        a = [1, 2, 3, 4, 5, 6]

        result = list(as_chunks(2, a))

        assert result == [[1, 2], [3, 4], [5, 6]]

        result = list(as_chunks(3, a))

        assert result == [[1, 2, 3], [4, 5, 6]]

        result = list(as_chunks(4, a))

        assert result == [[1, 2, 3, 4], [5, 6]]

        result = list(as_chunks(6, a))

        assert result == [a]

        result = list(as_chunks(18, a))

        assert result == [a]

        result = list(as_chunks(3, []))

        assert result == []

    def test_uniq(self):
        a = [1, 1, 2, 2, 2, 2, 3, 4, 4, 5, 2]

        result = list(uniq(a))

        assert result == [1, 2, 3, 4, 5, 2]

        result = list(uniq([1]))

        assert result == [1]

        result = list(uniq([]))

        assert result == []

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

    def test_with_is_first(self):
        a = [1, 2, 3, 4]

        result = list(with_is_first(a))

        assert result == [(True, 1), (False, 2), (False, 3), (False, 4)]

        result = list(with_is_first([1]))

        assert result == [(True, 1)]

        result = list(with_is_first([]))

        assert result == []

    def test_with_is_last(self):
        a = [1, 2, 3, 4]

        result = list(with_is_last(a))

        assert result == [(False, 1), (False, 2), (False, 3), (True, 4)]

        result = list(with_is_last([1]))

        assert result == [(True, 1)]

        result = list(with_is_last([]))

        assert result == []
