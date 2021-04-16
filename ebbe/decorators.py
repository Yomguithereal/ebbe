# =============================================================================
# Ebbe Decorators
# =============================================================================
#
from functools import wraps
from ebbe.iter import fail_fast as fail


def fail_fast(fn):

    @wraps(fn)
    def wrapped(*args, **kwargs):
        return fail(fn(*args, **kwargs))

    return wrapped


__all__ = [
    'fail_fast'
]
