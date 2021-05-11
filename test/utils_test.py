# =============================================================================
# Ebbe Utilities Unit Tests
# =============================================================================
import pytest

from ebbe import (
    getpath,
    pathgetter,
    sorted_uniq
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
    }
}


class TestUtils(object):
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
