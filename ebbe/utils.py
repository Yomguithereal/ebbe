# =============================================================================
# Ebbe Miscellaneous Helper Functions
# =============================================================================
#
from sys import version_info
from collections import OrderedDict
from collections.abc import Iterable

AT_LEAST_PY37 = version_info >= (3, 7)
DEFAULT_ORDERED_DICT = dict if AT_LEAST_PY37 else OrderedDict


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


def parse_path(string, *, split_char=".", parse_indices=False):
    path = string.split(split_char)

    if parse_indices:
        path = (parse_index(i) for i in path)

    return path


def getpath(
    target,
    path,
    default=None,
    *,
    items=True,
    attributes=False,
    split_char=None,
    parse_indices=False
):

    if split_char is not None:
        if isinstance(path, str):
            path = parse_path(path, split_char=split_char, parse_indices=parse_indices)
    else:
        if isinstance(path, str) or not isinstance(path, Iterable):
            raise TypeError

    for step in path:
        if items and callable(getattr(target, "__getitem__", None)):
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


def pathgetter(
    *paths,
    items=True,
    attributes=False,
    split_char=None,
    parse_indices=False,
    default=None
):

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
                target, paths[0], default, items=items, attributes=attributes
            )

    else:

        def operation(target, default=default):
            return tuple(
                getpath(target, path, default, items=items, attributes=attributes)
                for path in paths
            )

    return operation


def sorted_uniq(iterable, *, key=None, **kwargs):
    started = False
    last_k = None

    output = []

    for item in sorted(iterable, key=key, **kwargs):
        k = item

        if key is not None:
            k = key(item)

        if not started:
            started = True
            output.append(item)
        else:
            if k == last_k:
                continue
            output.append(item)

        last_k = k

    return output


def indexed(iterable, factory=dict, *, key=None):
    if not isinstance(iterable, Iterable):
        raise TypeError("target is not iterable")

    if not callable(factory):
        raise TypeError("factory is not callable")

    if key is not None and not callable(key):
        raise TypeError("key is not callable")

    index = factory()

    if key is not None:
        for item in iterable:
            k = key(item)
            index[k] = item
    else:
        for item in iterable:
            index[item] = item

    return index


def grouped(iterable, factory=dict, container=list, *, key=None, value=None):
    if not isinstance(iterable, Iterable):
        raise TypeError("target is not iterable")

    if not callable(factory):
        raise TypeError("factory is not callable")

    if not callable(container):
        raise TypeError("container is not callable")

    if key is not None and not callable(key):
        raise TypeError("key is not callable")

    if value is not None and not callable(value):
        raise TypeError("value is not callable")

    groups = factory()

    if hasattr(container, "add") and callable(container.add):
        adder = container.add
    elif hasattr(container, "append") and callable(container.append):
        adder = container.append
    else:
        raise TypeError("unknown container")

    for item in iterable:
        k = key(item) if key is not None else item
        c = groups.get(k)

        if c is None:
            c = container()
            groups[k] = c

        v = item if value is None else value(item)
        adder(c, v)

    return groups


def partitioned(
    iterable, factory=DEFAULT_ORDERED_DICT, container=list, *, key=None, value=None
):
    groups = grouped(iterable, factory, container, key=key, value=value)
    return list(groups.values())


def grouped_items(iterable, factory=dict, container=list):
    if not isinstance(iterable, Iterable):
        raise TypeError("target is not iterable")

    if not callable(factory):
        raise TypeError("factory is not callable")

    if not callable(container):
        raise TypeError("container is not callable")

    groups = factory()

    if hasattr(container, "add") and callable(container.add):
        adder = container.add
    elif hasattr(container, "append") and callable(container.append):
        adder = container.append
    else:
        raise TypeError("unknown container")

    for k, v in iterable:
        c = groups.get(k)

        if c is None:
            c = container()
            groups[k] = c

        adder(c, v)

    return groups


def partitioned_items(iterable, factory=DEFAULT_ORDERED_DICT, container=list):
    groups = grouped_items(iterable, factory, container)
    return list(groups.values())
