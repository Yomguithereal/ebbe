# =============================================================================
# Ebbe Decorators Unit Tests
# =============================================================================
import pytest
from ebbe.decorators import fail_fast, with_defer


class TestDecorators(object):
    def test_fail_fast(self):
        @fail_fast()
        def hellraiser():
            raise RuntimeError
            yield 1

        with pytest.raises(RuntimeError):
            hellraiser()

    def test_with_defer(self):
        values = []

        @with_defer()
        def operation(a, b, *, defer):
            defer(lambda: values.append(10))
            values.append(a + b)

        operation(3, 4)
        operation(4, 4)
        operation(3, 6)

        assert values == [7, 10, 8, 10, 9, 10]
