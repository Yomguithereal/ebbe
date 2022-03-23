# =============================================================================
# Ebbe Decorators
# =============================================================================
#
from functools import wraps
from contextlib import ExitStack

from ebbe.iter import fail_fast as fail


def fail_fast():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            return fail(fn(*args, **kwargs))

        return wrapped

    return wrapper


def with_defer():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            with ExitStack() as stack:
                defer = stack.callback
                kwargs["defer"] = defer
                fn(*args, **kwargs)

        return wrapped

    return wrapper


__all__ = ["fail_fast", "with_defer"]
