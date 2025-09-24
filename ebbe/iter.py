# =============================================================================
# Ebbe Iterating Functions
# =============================================================================
#
from typing import (
    Any,
    Iterator,
    Iterable,
    List,
    Union,
    Tuple,
    TypeVar,
    Optional,
    Callable,
    Sequence,
    overload,
)

from collections import deque

T = TypeVar("T")
W = TypeVar("W")
V = TypeVar("V")


def empty_generator() -> Iterator:
    yield from ()


def as_chunks(size: int, iterable: Iterable[T]) -> Iterator[List[T]]:
    chunk = []

    for item in iterable:
        if len(chunk) == size:
            yield chunk
            chunk = []

        chunk.append(item)

    if chunk:
        yield chunk


def as_reconciled_chunks(
    size: int,
    iterable: Iterable[T],
    work: Callable[[List[T]], W],
    reconcile: Callable[[W, T], V],
) -> Iterator[Tuple[T, V]]:
    for chunk in as_chunks(size, iterable):
        data = work(chunk)

        for item in chunk:
            reconciled = reconcile(data, item)

            yield item, reconciled


# NOTE: this function makes the following assumptions:
#   1. the work done is single-threaded
#   2. items are emitted in the same order they are given
def outer_zip(
    complex_iterable: Iterable[T],
    key: Callable[[T], W],
    work: Callable[[Iterator[W]], Iterator[V]],
) -> Iterator[Tuple[T, V]]:
    queue = deque()

    def simple_iterable():
        for item in complex_iterable:
            queue.append(item)
            yield key(item)

    for result in work(simple_iterable()):
        item = queue.popleft()
        yield item, result


@overload
def as_grams(size: int, iterable: str) -> Iterator[str]:
    ...


@overload
def as_grams(size: int, iterable: List[T]) -> Iterator[List[T]]:
    ...


@overload
def as_grams(size: int, iterable: Sequence[T]) -> Iterator[Sequence[T]]:
    ...


@overload
def as_grams(size: int, iterable: Iterable[T]) -> Iterator[Tuple[T]]:
    ...


def as_grams(
    size: int, iterable: Union[Iterable[T], Sequence[T]]
) -> Union[Iterator[str], Iterator[List[T]], Iterator[Tuple[T]], Iterator[Sequence[T]]]:
    # For sized sequences
    if isinstance(iterable, Sequence):
        l = len(iterable)

        if l == 0:
            return

        if l < size:
            yield iterable[:]

        for i in range(l - size + 1):
            yield iterable[i : i + size]

    # For lazy iterables
    else:
        iterator = iter(iterable)
        buffer = deque()

        while len(buffer) < size:
            try:
                buffer.append(next(iterator))
            except StopIteration:
                if buffer:
                    yield tuple(i for i in buffer)

                return

        for item in iterator:
            yield tuple(i for i in buffer)
            buffer.popleft()
            buffer.append(item)

        yield tuple(i for i in buffer)


def fail_fast(iterable: Iterable[T]) -> Iterator[T]:
    iterator = iter(iterable)

    try:
        first_item = next(iterator)
    except StopIteration:
        return empty_generator()

    def generator():
        yield first_item
        yield from iterator

    return generator()


def uniq(
    iterable: Iterable[T], *, key: Optional[Callable[[T], Any]] = None
) -> Iterator[T]:
    last_k = None

    for is_first, item in with_is_first(iterable):
        k = item

        if key is not None:
            k = key(item)

        if is_first:
            yield item
        else:
            if last_k == k:
                continue

            yield item

        last_k = k


def distinct(
    iterable: Iterable[T], *, key: Optional[Callable[[T], Any]] = None
) -> Iterator[T]:
    already_seen = set()

    for item in iterable:
        k = item

        if key is not None:
            k = key(item)

        if k in already_seen:
            continue

        already_seen.add(k)
        yield item


def with_prev(iterable: Iterable[T]) -> Iterator[Tuple[Optional[T], T]]:
    prev = None

    for item in iterable:
        yield prev, item

        prev = item


def with_next(iterable: Iterable[T]) -> Iterator[Tuple[T, Optional[T]]]:
    iterator = iter(iterable)

    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield last, item
        last = item

    yield last, None


def with_prev_and_next(
    iterable: Iterable[T],
) -> Iterator[Tuple[Optional[T], T, Optional[T]]]:
    prev = None
    iterator = iter(iterable)

    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield prev, last, item
        prev = last
        last = item

    yield prev, last, None


def with_is_first(iterable: Iterable[T]) -> Iterator[Tuple[bool, T]]:
    is_first = True

    for item in iterable:
        yield is_first, item
        is_first = False


def with_is_last(iterable: Iterable[T]) -> Iterator[Tuple[bool, T]]:
    iterator = iter(iterable)

    try:
        last = next(iterator)
    except StopIteration:
        return

    for item in iterator:
        yield False, last
        last = item

    yield True, last


def without_first(iterable: Iterable[T]) -> Iterator[T]:
    for is_first, item in with_is_first(iterable):
        if is_first:
            continue

        yield item


def without_last(iterable: Iterable[T]) -> Iterator[T]:
    for is_last, item in with_is_last(iterable):
        if is_last:
            break

        yield item
