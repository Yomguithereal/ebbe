# =============================================================================
# Ebbe Decorators Unit Tests
# =============================================================================
import pytest
from ebbe.decorators import fail_fast


class TestDecorators(object):
    def test_fail_fast(self):

        @fail_fast
        def hellraiser():
            raise RuntimeError
            yield 1

        with pytest.raises(RuntimeError):
            hellraiser()
