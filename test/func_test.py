# =============================================================================
# Ebbe Functional Helpers Unit Tests
# =============================================================================
from pytest import raises

from ebbe.func import noop, count_arity, compose, rcompose


class TestFunc(object):
    def test_count_arity(self):
        def zero():
            ...

        def one(a):
            ...

        def two(a, b):
            ...

        def three(a, b, c):
            ...

        def kw(a, test=True):
            ...

        assert count_arity(noop) == 2
        assert count_arity(zero) == 0
        assert count_arity(one) == 1
        assert count_arity(two) == 2
        assert count_arity(three) == 3
        assert count_arity(kw) == 1

    def test_compose(self):
        def times_2(x):
            return x * 2

        def plus_5(x):
            return x + 5

        # def wrong_arity(x, y):
        #     ...

        with raises(TypeError, match="least"):
            compose()

        with raises(TypeError, match="callables"):
            compose(None, 45)

        assert compose(times_2)(5) == 10
        assert compose(times_2, plus_5)(10) == 30
        assert compose(times_2, plus_5, reverse=True)(10) == 25
        assert rcompose(times_2, plus_5)(10) == 25
