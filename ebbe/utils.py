# =============================================================================
# Ebbe Miscellaneous Helper Functions
# =============================================================================
#
from collections.abc import Iterable

from ebbe.iter import uniq


def noop(*args, **kwargs):
    pass


def parse_index(value):
    try:
        return int(value)
    except ValueError:
        return value


def parse_path(string, *, split_char='.', parse_indices=False):
    path = string.split(split_char)

    if parse_indices:
        path = (parse_index(i) for i in path)

    return path


def getpath(target, path, default=None, *, items=True, attributes=False,
            split_char=None, parse_indices=False):

    if split_char is not None:
        if isinstance(path, str):
            path = parse_path(path, split_char=split_char, parse_indices=parse_indices)
    else:
        if isinstance(path, str) or not isinstance(path, Iterable):
            raise TypeError

    for step in path:
        if items and callable(getattr(target, '__getitem__', None)):
            try:
                target = target[step]
            except (IndentationError, KeyError):
                return default
        elif attributes:
            try:
                target = getattr(target, step)
            except (AttributeError, TypeError):
                return default
        else:
            return default

    return target


def pathgetter(*paths, items=True, attributes=False, split_char=None,
               parse_indices=False):

    if not paths:
        raise TypeError

    # Preparsing paths
    if split_char is not None:
        paths = [
            list(parse_path(p, split_char=split_char, parse_indices=parse_indices))
            for p in paths
        ]

    if len(paths) == 1:
        def operation(target, default=None):
            return getpath(
                target,
                paths[0],
                default,
                items=items,
                attributes=attributes
            )
    else:
        def operation(target, default=None):
            return tuple(
                getpath(
                    target,
                    path,
                    default,
                    items=items,
                    attributes=attributes
                )
                for path in paths
            )

    return operation


def sorted_uniq(seq, **kwargs):
    return list(uniq(sorted(seq, **kwargs)))
