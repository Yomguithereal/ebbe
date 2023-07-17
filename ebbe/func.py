# =============================================================================
# Ebbe Functional Helpers
# =============================================================================
#
from typing import Callable, TypeVar, Any

from inspect import signature, Parameter

T = TypeVar("T")


def noop(*args: Any, **kwargs: Any) -> None:
    pass


def count_arity(fn: Callable) -> int:
    parameters = signature(fn).parameters

    return sum(1 if p.default == Parameter.empty else 0 for p in parameters.values())


def compose(*fns: Callable[[T], T], reverse: bool = False) -> Callable[[T], T]:
    if len(fns) < 1:
        raise TypeError("compose expects at least one callable")

    if any(not callable(fn) for fn in fns):
        raise TypeError("compose is expecting callables")

    def chain(arg: T) -> T:
        nonlocal fns

        if not reverse:
            fns = reversed(fns)  # type: ignore

        for fn in fns:
            arg = fn(arg)

        return arg

    return chain


def rcompose(*fns: Callable[[T], T], reverse=False) -> Callable[[T], T]:
    return compose(*fns, reverse=not reverse)
