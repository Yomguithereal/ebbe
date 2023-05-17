# =============================================================================
# Ebbe Functional Helpers
# =============================================================================
#
from inspect import signature, Parameter


def noop(*args, **kwargs):
    pass


def count_arity(fn) -> int:
    parameters = signature(fn).parameters

    return sum(1 if p.default == Parameter.empty else 0 for p in parameters.values())


def compose(*fns, reverse=False):
    if len(fns) < 1:
        raise TypeError("compose expects at least one callable")

    if any(not callable(fn) for fn in fns):
        raise TypeError("compose is expecting callables")

    def chain(arg):
        nonlocal fns

        if not reverse:
            fns = reversed(fns)

        for fn in fns:
            arg = fn(arg)

        return arg

    return chain


def rcompose(*fns, reverse=False):
    return compose(*fns, reverse=not reverse)
