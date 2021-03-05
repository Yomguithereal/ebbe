# =============================================================================
# Ebbe Functions
# =============================================================================
#


def with_prev(iterable):
    prev = None

    for item in iterable:
        yield prev, item

        prev = item


def with_next(iterable):
    iterator = iter(iterable)

    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield last, item
        last = item

    yield last, None


def with_is_first(iterable):
    is_first = True

    for item in iterable:
        yield is_first, item
        is_first = False


def with_is_last(iterable):
    iterator = iter(iterable)

    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield False, last
        last = item

    yield True, last


# TODO: as_chunks
