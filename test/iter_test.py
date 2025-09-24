# =============================================================================
# Ebbe Iterating Functions Unit Tests
# =============================================================================
import pytest
from operator import itemgetter

from ebbe import (
    as_chunks,
    as_reconciled_chunks,
    outer_zip,
    as_grams,
    fail_fast,
    uniq,
    distinct,
    with_prev,
    with_prev_and_next,
    with_next,
    with_is_first,
    with_is_last,
    without_first,
    without_last,
)

STRING = "Bonjour"

STRING_TESTS = [
    ("B", "o", "n", "j", "o", "u", "r"),
    ("Bo", "on", "nj", "jo", "ou", "ur"),
    ("Bon", "onj", "njo", "jou", "our"),
    ("Bonj", "onjo", "njou", "jour"),
]

SENTENCE = tuple("the cat eats the mouse".split(" "))

SENTENCE_TEST = [
    (("the",), ("cat",), ("eats",), ("the",), ("mouse",)),
    (("the", "cat"), ("cat", "eats"), ("eats", "the"), ("the", "mouse")),
    (("the", "cat", "eats"), ("cat", "eats", "the"), ("eats", "the", "mouse")),
    (("the", "cat", "eats", "the"), ("cat", "eats", "the", "mouse")),
]


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

    def test_as_reconciled_chunks(self):
        data = [1, 2, 3, 4, 5, 6]

        def work(chunk):
            return {n: True for n in chunk if n % 2 == 0}

        def reconcile(data, item):
            return data.get(item)

        for size in range(1, 7):
            assert list(as_reconciled_chunks(size, data, work, reconcile)) == [
                (1, None),
                (2, True),
                (3, None),
                (4, True),
                (5, None),
                (6, True),
            ]

    def test_outer_zip(self):
        data = [("one", 1), ("two", 2), ("three", 3)]

        output = []

        def work(items):
            for chunk in as_chunks(2, items):
                for item in chunk:
                    yield item * 2

        for original_item, result in outer_zip(data, key=lambda p: p[1], work=work):
            output.append((original_item[0], result))

        assert output == [("one", 2), ("two", 4), ("three", 6)]

    def test_as_grams(self):
        for i in range(4):
            assert tuple(as_grams(i + 1, STRING)) == STRING_TESTS[i]
            assert tuple(as_grams(i + 1, SENTENCE)) == SENTENCE_TEST[i]

        assert list(as_grams(4, "")) == []
        assert list(as_grams(4, "te")) == ["te"]
        assert list(as_grams(4, "test")) == ["test"]
        assert list(as_grams(4, "teste")) == ["test", "este"]

        for i in range(4):
            assert tuple(as_grams(i + 1, (w for w in SENTENCE))) == SENTENCE_TEST[i]

        assert list(as_grams(4, iter([]))) == []
        assert list(as_grams(4, iter(SENTENCE[:2]))) == [("the", "cat")]
        assert list(as_grams(4, iter(SENTENCE[:3]))) == [("the", "cat", "eats")]
        assert list(as_grams(4, iter(SENTENCE[:4]))) == [("the", "cat", "eats", "the")]
        assert list(as_grams(4, iter(SENTENCE[:5]))) == [
            ("the", "cat", "eats", "the"),
            ("cat", "eats", "the", "mouse"),
        ]

        assert list(as_grams(2, (i * 2 for i in range(5)))) == [
            (0, 2),
            (2, 4),
            (4, 6),
            (6, 8),
        ]

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

        tuples = [(11, 23), (1, 2), (2, 2), (3, 2), (1, 5), (1, 6)]

        result = list(uniq(tuples, key=itemgetter(1)))

        assert result == [(11, 23), (1, 2), (1, 5), (1, 6)]

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

    def test_without_last(self):
        a = [1, 2, 3]

        result = list(without_last(a))

        assert result == [1, 2]

        assert list(without_last([1])) == []

        assert list(without_last([])) == []
