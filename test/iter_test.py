# =============================================================================
# Ebbe Iterating Functions Unit Tests
# =============================================================================
import pytest
from operator import itemgetter

from ebbe import (
    as_chunks,
    fail_fast,
    uniq,
    distinct,
    with_prev,
    with_prev_and_next,
    with_next,
    with_is_first,
    with_is_last,
    without_first
)


class TestIter(object):
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

    def test_fail_fast(self):
        def hellraiser():
            raise RuntimeError
            yield 1

        hellraiser()

        with pytest.raises(RuntimeError):
            fail_fast(hellraiser())

        assert list(fail_fast([1, 2, 3])) == [1, 2, 3]
        assert list(fail_fast([1])) == [1]
        assert list(fail_fast([])) == []

    def test_uniq(self):
        a = [1, 1, 2, 2, 2, 2, 3, 4, 4, 5, 2]

        result = list(uniq(a))

        assert result == [1, 2, 3, 4, 5, 2]

        result = list(uniq([1]))

        assert result == [1]

        result = list(uniq([]))

        assert result == []

    def test_distinct(self):
        a = [(1, 4), (1, 5), (2, 3), (4, 5), (2, 7), (6, 8), (2, 3)]

        result = list(distinct(a))
        assert result == [(1, 4), (1, 5), (2, 3), (4, 5), (2, 7), (6, 8)]

        result = list(distinct(a, key=itemgetter(0)))
        assert result == [(1, 4), (2, 3), (4, 5), (6, 8)]

        result = list(distinct(range(4), key=lambda x: x % 2))
        assert result == [0, 1]

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

    def test_with_prev_and_next(self):
        a = [1, 2, 3, 4]

        result = list(with_prev_and_next(a))

        assert result == [(None, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, None)]

        result = list(with_prev_and_next([1]))

        assert result == [(None, 1, None)]

        result = list(with_prev_and_next([]))

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

    def test_without_first(self):
        a = [1, 2, 3]

        result = list(without_first(a))

        assert result == [2, 3]

        assert list(without_first([1])) == []

        assert list(without_first([])) == []
