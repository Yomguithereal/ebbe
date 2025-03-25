# =============================================================================
# Ebbe Miscellaneous Helper Functions
# =============================================================================
#
from typing import (
    Optional,
    Dict,
    Mapping,
    MutableMapping,
    Sequence,
    Container,
    Collection,
    Iterable,
    TypeVar,
    Union,
    List,
    Tuple,
    Set,
    Any,
    Callable,
    Type,
    overload,
)
from ebbe.types import Protocol

from sys import version_info
from collections import OrderedDict

AT_LEAST_PY37 = version_info >= (3, 7)
DEFAULT_ORDERED_DICT = dict if AT_LEAST_PY37 else OrderedDict
NOT_FOUND = object()

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
D = TypeVar("D")
GD = TypeVar("GD", covariant=True)

KeyOrIndex = Union[str, int]
Path = Union[KeyOrIndex, Iterable[KeyOrIndex]]

Gettable = Union[Mapping[K, V], Sequence[V]]


@overload
def get(target: Mapping[K, V], key: K, default: None = ...) -> Optional[V]:
    ...


@overload
def get(target: Mapping[K, V], key: K, default: D = ...) -> Union[V, D]:
    ...


@overload
def get(target: Sequence[V], key: int, default: None = ...) -> Optional[V]:
    ...


@overload
def get(target: Sequence[V], key: int, default: D = ...) -> Union[V, D]:
    ...


def get(
    target: Gettable[K, V], key: K, default: Optional[D] = None
) -> Optional[Union[V, D]]:
    try:
        return target[key]  # type: ignore
    except (KeyError, IndexError):
        return default


class Getter(Protocol[K, GD]):
    @overload
    def __call__(self, target: Mapping[K, V], default: None = ...) -> Union[V, GD]:
        ...

    @overload
    def __call__(self, target: Mapping[K, V], default: D = ...) -> Union[V, D]:
        ...

    @overload
    def __call__(self, target: Sequence[V], default: None = ...) -> Union[V, GD]:
        ...

    @overload
    def __call__(self, target: Sequence[V], default: D = ...) -> Union[V, D]:
        ...

    def __call__(
        self, target: Gettable[K, V], default: Optional[D] = None
    ) -> Union[V, D, GD]:
        ...


@overload
def getter(key: K, default: None = ...) -> Getter[K, None]:
    ...


@overload
def getter(key: K, default: GD = ...) -> Getter[K, GD]:
    ...


def getter(key: K, default: Optional[GD] = None) -> Getter[K, GD]:
    def operation(target, default=default):
        try:
            return target[key]
        except (KeyError, IndexError):
            return default

    return operation


def parse_index(value: str) -> Union[str, int]:
    try:
        return int(value)
    except ValueError:
        return value


def parse_path(
    string: str, *, split_char: str = ".", parse_indices: bool = False
) -> Iterable[Union[str, int]]:
    path = string.split(split_char)

    if parse_indices:
        path = (parse_index(i) for i in path)

    return path


def getpath(
    target: Any,
    path: Path,
    default: Optional[Any] = None,
    *,
    items: bool = True,
    attributes: bool = False,
    split_char: Optional[str] = None,
    parse_indices: bool = False
) -> Any:
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


class PathGetter(Protocol):
    def __call__(self, target: Any, default: Optional[Any] = ...) -> Any:
        ...


def pathgetter(
    path: Path,
    items: bool = True,
    attributes: bool = False,
    split_char: Optional[str] = None,
    parse_indices: bool = False,
    default: Optional[Any] = None,
) -> PathGetter:
    # Preparsing paths
    if split_char is not None:
        path = parse_path(path, split_char=split_char, parse_indices=parse_indices)

    def operation(target, default=default):
        return getpath(target, path, default, items=items, attributes=attributes)

    return operation


class PathsGetter(Protocol):
    def __call__(self, target: Any, default: Optional[Any] = ...) -> Tuple[Any]:
        ...


def pathsgetter(
    *paths: Path,
    items: bool = True,
    attributes: bool = False,
    split_char: Optional[str] = None,
    parse_indices: bool = False,
    default: Optional[Any] = None
) -> PathsGetter:
    # Preparsing paths
    if split_char is not None:
        paths = [
            list(parse_path(p, split_char=split_char, parse_indices=parse_indices))
            for p in paths
        ]  # type: ignore

    def operation(target, default=default):
        return tuple(
            getpath(target, path, default, items=items, attributes=attributes)
            for path in paths
        )

    return operation


def sorted_uniq(
    iterable: Iterable[T],
    *,
    key: Optional[Callable[[T], Any]] = None,
    reverse: bool = False
) -> List[T]:
    started = False
    last_k = None

    output = []

    for item in sorted(iterable, key=key, reverse=reverse):
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


@overload
def indexed(iterable: Iterable[V], *, key: None = ...) -> Dict[V, V]:
    ...


@overload
def indexed(iterable: Iterable[V], *, key: Callable[[V], K] = ...) -> Dict[K, V]:
    ...


@overload
def indexed(
    iterable: Iterable[V], factory: Type[MutableMapping] = ..., *, key: None = ...
) -> MutableMapping[V, V]:
    ...


@overload
def indexed(
    iterable: Iterable[V],
    factory: Type[MutableMapping] = ...,
    *,
    key: Callable[[V], K] = ...
) -> MutableMapping[K, V]:
    ...


def indexed(
    iterable: Iterable[V],
    factory: Type = dict,
    *,
    key: Optional[Callable[[V], K]] = None
) -> Union[MutableMapping[K, V], MutableMapping[V, V]]:
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


@overload
def grouped(iterable: Iterable[T]) -> Dict[T, List[T]]:
    ...


@overload
def grouped(iterable: Iterable[T], *, key: Callable[[T], K]) -> Dict[K, List[T]]:
    ...


@overload
def grouped(iterable: Iterable[T], *, value: Callable[[T], V]) -> Dict[T, List[V]]:
    ...


@overload
def grouped(
    iterable: Iterable[T], *, key: Callable[[T], K], value: Callable[[T], V]
) -> Dict[K, List[V]]:
    ...


@overload
def grouped(
    iterable: Iterable[T], factory: Type[Dict] = ..., container: Type[Set] = ...
) -> Dict[T, Set[T]]:
    ...


@overload
def grouped(
    iterable: Iterable[T],
    factory: Type[Dict] = ...,
    container: Type[Set] = ...,
    *,
    key: Callable[[T], K]
) -> Dict[K, Set[T]]:
    ...


@overload
def grouped(
    iterable: Iterable[T],
    factory: Type[Dict] = ...,
    container: Type[Set] = ...,
    *,
    value: Callable[[T], V]
) -> Dict[T, Set[V]]:
    ...


@overload
def grouped(
    iterable: Iterable[T],
    factory: Type[Dict] = ...,
    container: Type[Set] = ...,
    *,
    key: Callable[[T], K],
    value: Callable[[T], V]
) -> Dict[K, Set[V]]:
    ...


def grouped(
    iterable: Iterable[T],
    factory: Type = dict,
    container: Type = list,
    *,
    key: Optional[Callable[[T], Any]] = None,
    value: Optional[Callable[[T], Any]] = None
) -> MutableMapping:
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
    iterable: Iterable[T],
    factory: Type = DEFAULT_ORDERED_DICT,
    container: Type = list,
    *,
    key: Optional[Callable[[T], Any]] = None,
    value: Optional[Callable[[T], V]] = None
) -> Union[List[Collection[T]], List[Collection[V]]]:
    groups = grouped(iterable, factory, container, key=key, value=value)
    return list(groups.values())  # type: ignore


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


def pick(d: Dict[K, V], keys: Iterable[K], *, strict: bool = False) -> Dict[K, V]:
    n = {}

    for k in keys:
        v = d.get(k, NOT_FOUND)

        if v is NOT_FOUND:
            if strict:
                raise KeyError(k)
            else:
                continue

        n[k] = v

    return n


def omit(d: Dict[K, V], keys: Container[K]) -> Dict[K, V]:
    n = {}

    for k, v in d.items():
        if k not in keys:
            n[k] = v

    return n
