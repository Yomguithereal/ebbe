# =============================================================================
# Ebbe Functions
# =============================================================================
#


def as_chunks(size, iterable):
    chunk = []

    for item in iterable:
        if len(chunk) == size:
            yield chunk
            chunk = []

        chunk.append(item)

    if chunk:
        yield chunk


def uniq(iterable):
    current_item = None

    for is_first, item in with_is_first(iterable):
        if is_first:
            yield item
            current_item = item
        else:
            if current_item == item:
                continue

            current_item = item
            yield item


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
