# =============================================================================
# Ebbe Miscellaneous Helper Functions
# =============================================================================
#
from collections import defaultdict
from collections.abc import Iterable

from ebbe.iter import uniq


def noop(*args, **kwargs):
    pass


def get(target, key, default=None):
    try:
        return target[key]
    except (KeyError, IndexError):
        return default


def getter(key, default=None):
    def operation(target, default=default):
        try:
            return target[key]
        except (KeyError, IndexError):
            return default

    return operation


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
            except (IndexError, KeyError):
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
               parse_indices=False, default=None):

    if not paths:
        raise TypeError

    # Preparsing paths
    if split_char is not None:
        paths = [
            list(parse_path(p, split_char=split_char, parse_indices=parse_indices))
            for p in paths
        ]

    if len(paths) == 1:
        def operation(target, default=default):
            return getpath(
                target,
                paths[0],
                default,
                items=items,
                attributes=attributes
            )
    else:
        def operation(target, default=default):
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


def indexed(iterable, factory=dict, *, key=None):
    if not isinstance(iterable, Iterable):
        raise TypeError('target is not iterable')

    if not callable(factory):
        raise TypeError('factory is not callable')

    if not callable(key):
        raise TypeError('key is not callable')

    index = factory()

    for item in iterable:
        k = key(item)
        index[k] = item

    return index


def grouped(iterable, factory=list, *, key=None):
    if not isinstance(iterable, Iterable):
        raise TypeError('target is not iterable')

    if not callable(factory):
        raise TypeError('factory is not callable')

    if not callable(key):
        raise TypeError('key is not callable')

    groups = defaultdict(factory)

    if hasattr(factory, 'add') and callable(factory.add):
        adder = factory.add
    elif hasattr(factory, 'append') and callable(factory.append):
        adder = factory.append
    else:
        raise TypeError('unknown container')

    for item in iterable:
        k = key(item)
        adder(groups[k], item)

    return groups
