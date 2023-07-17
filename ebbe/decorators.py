# =============================================================================
# Ebbe Decorators
# =============================================================================
#
from typing import Callable, TypeVar, Iterator, Any
from ebbe.types import ParamSpec

from functools import wraps
from contextlib import ExitStack

from ebbe.iter import fail_fast as fail

T = TypeVar("T")
P = ParamSpec("P")


def fail_fast() -> Callable[[Callable[P, Iterator[T]]], Callable[P, Iterator[T]]]:
    def wrapper(fn: Callable[P, Iterator[T]]) -> Callable[P, Iterator[T]]:
        @wraps(fn)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> Iterator[T]:
            return fail(fn(*args, **kwargs))

        return wrapped

    return wrapper


F = TypeVar("F", bound=Callable[..., Any])


def with_defer() -> Callable[[F], F]:
    def wrapper(fn: F) -> F:
        @wraps(fn)
        def wrapped(*args, **kwargs):
            with ExitStack() as stack:
                defer = stack.callback
                kwargs["defer"] = defer
                return fn(*args, **kwargs)

        return wrapped  # type: ignore

    return wrapper


__all__ = ["fail_fast", "with_defer"]
