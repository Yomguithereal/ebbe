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

# TODO: with_is_first, with_is_last, as_chunks
