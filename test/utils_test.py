# =============================================================================
# Ebbe Utilities Unit Tests
# =============================================================================
import pytest
from collections import OrderedDict
from itertools import chain

from ebbe import (
    get,
    getter,
    getpath,
    pathgetter,
    sorted_uniq,
    indexed,
    grouped
)


class Container(object):
    def __init__(self, value, recurse=True):
        self.value = value
        self.numbers = [4, 5, 6]

        if recurse:
            self.recursion = Container(self.value, recurse=False)


NESTED_OBJECT = {
    'a': {
        'b': [{'c': 4}, 45, {'f': [1, 2, 3]}],
        'd': {
            'e': 5,
            'g': Container(45)
        }
    },
    't': 32
}


class TestUtils(object):
    def test_get(self):
        assert get(NESTED_OBJECT, 't') == 32
        assert get(NESTED_OBJECT, 'l') is None
        assert get(NESTED_OBJECT, 'l', 27) == 27

        assert get([0, 2, 4], 1) == 2
        assert get([0, 2, 4], 7) is None

    def test_getter(self):
        assert getter('t')(NESTED_OBJECT) == 32
        assert getter('l')(NESTED_OBJECT) is None
        assert getter('l', 27)(NESTED_OBJECT) == 27
        assert getter('l')(NESTED_OBJECT, 28) == 28
        assert getter('l', 27)(NESTED_OBJECT, 28) == 28

    def test_getpath(self):
        with pytest.raises(TypeError):
            getpath(NESTED_OBJECT, 'test')

        assert getpath(NESTED_OBJECT, ['a', 'd', 'e']) == 5
        assert getpath(NESTED_OBJECT, ['a', 'd', 'e'], items=None) is None
        assert getpath(NESTED_OBJECT, ['a', 'c']) is None
        assert getpath(NESTED_OBJECT, ['a', 'c'], 67) == 67
        assert getpath(NESTED_OBJECT, ['a', 'b', 1]) == 45
        assert getpath(NESTED_OBJECT, ['a', 'b', -1, 'f', -1]) == 3
        assert getpath(NESTED_OBJECT, ['a', 'b', 0, 'c']) == 4
        assert getpath(NESTED_OBJECT, ['a', 'd', 'g', 'numbers', 1]) is None
        assert getpath(NESTED_OBJECT, ['a', 'd', 'g', 'numbers', 1], attributes=True) == 5
        assert getpath(NESTED_OBJECT, ['a', 'd', 'g', 3], attributes=True) is None
        assert getpath(NESTED_OBJECT, ['a', 'd', 'g', 'recursion', 'numbers'], attributes=True) == [4, 5, 6]
        assert getpath(NESTED_OBJECT, 'a.d.e', split_char='.') == 5
        assert getpath(NESTED_OBJECT, 'a§d§e', split_char='§') == 5
        assert getpath(NESTED_OBJECT, 'a.b.1', split_char='.', parse_indices=True) == 45
        assert getpath(NESTED_OBJECT, 'a.b.-1.f.-1', split_char='.', parse_indices=True) == 3

        assert getpath([[1, 2]], [3, 4, 17]) is None

    def test_pathgetter(self):
        with pytest.raises(TypeError):
            pathgetter()

        assert pathgetter(['a', 'd', 'e'])(NESTED_OBJECT) == 5
        assert pathgetter(['a', 'd', 'e'], items=None)(NESTED_OBJECT) is None
        assert pathgetter(['a', 'c'])(NESTED_OBJECT) is None
        assert pathgetter(['a', 'c'])(NESTED_OBJECT, 67) == 67
        assert pathgetter(['a', 'b', 1])(NESTED_OBJECT) == 45
        assert pathgetter(['a', 'b', -1, 'f', -1])(NESTED_OBJECT) == 3
        assert pathgetter(['a', 'b', 0, 'c'])(NESTED_OBJECT) == 4
        assert pathgetter(['a', 'd', 'g', 'numbers', 1])(NESTED_OBJECT) is None
        assert pathgetter(['a', 'd', 'g', 'numbers', 1], attributes=True)(NESTED_OBJECT) == 5
        assert pathgetter(['a', 'd', 'g', 3], attributes=True)(NESTED_OBJECT) is None
        assert pathgetter(['a', 'd', 'g', 'recursion', 'numbers'], attributes=True)(NESTED_OBJECT) == [4, 5, 6]
        assert pathgetter('a.d.e', split_char='.')(NESTED_OBJECT) == 5
        assert pathgetter('a§d§e', split_char='§')(NESTED_OBJECT) == 5
        assert pathgetter('a.b.1', split_char='.', parse_indices=True)(NESTED_OBJECT) == 45
        assert pathgetter('a.b.-1.f.-1', split_char='.', parse_indices=True)(NESTED_OBJECT) == 3

        tuple_getter = pathgetter(
            ['a', 'd', 'e'],
            ['a', 'c'],
            ['a', 'b', 1]
        )

        assert tuple_getter(NESTED_OBJECT) == (5, None, 45)

        default_getter = pathgetter(['a', 'd', 'e'], default=1337)

        assert default_getter(NESTED_OBJECT) == 5
        assert default_getter({}) == 1337

    def test_sorted_uniq(self):
        numbers = [3, 17, 3, 4, 1, 4, 5, 5, 1, -1, 5]

        assert sorted_uniq(numbers) == [-1, 1, 3, 4, 5, 17]
        assert sorted_uniq(numbers, reverse=True) == [17, 5, 4, 3, 1, -1]

    def test_indexed(self):
        with pytest.raises(TypeError):
            indexed(None)

        with pytest.raises(TypeError):
            indexed([], None)

        with pytest.raises(TypeError):
            indexed([])

        with pytest.raises(TypeError):
            indexed([], key='test')

        assert indexed(range(3), key=lambda x: x * 10) == {0: 0, 10: 1, 20: 2}
        ordered = indexed(range(3), OrderedDict, key=lambda x: x * 10)

        assert isinstance(ordered, OrderedDict)
        assert ordered == OrderedDict([(0, 0), (10, 1), (20, 2)])

        assert indexed(range(3), key=lambda x: x * 10) == {x * 10: x for x in range(3)}

    def test_grouped(self):
        with pytest.raises(TypeError):
            grouped(None)

        with pytest.raises(TypeError):
            grouped([], None)

        with pytest.raises(TypeError):
            grouped([])

        with pytest.raises(TypeError):
            grouped([], key='test')

        assert grouped(range(5), key=lambda x: 'ok' if x in [2, 3] else 'not-ok') == {
            'ok': [2, 3],
            'not-ok': [0, 1, 4]
        }

        assert grouped(chain(range(5), range(5)), set, key=lambda x: 'ok' if x in [2, 3] else 'not-ok') == {
            'ok': {2, 3},
            'not-ok': {0, 1, 4}
        }
