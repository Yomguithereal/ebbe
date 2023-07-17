from typing import TypeVar, Hashable

import sys

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

if sys.version_info >= (3, 10):
    from typing import ParamSpec, Concatenate
else:
    from typing_extensions import ParamSpec, Concatenate

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class Indexable(Protocol[K, V]):
    def __getitem__(self, key: K) -> V:
        ...
