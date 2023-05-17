# =============================================================================
# Ebbe Formatting Helpers
# =============================================================================
#
from typing import Iterable, Iterator, Optional, Union, Tuple, List, Container, Any
from functools import partial


def format_int(n: float, separator: str = ",") -> str:
    s = "{:,}".format(int(n))

    if separator != ",":
        return s.replace(",", separator)

    return s


def and_join(v: Iterable[str], separator: str = ",", copula: str = "and"):
    if not isinstance(v, list):
        v = list(v)

    if len(v) < 2:
        return separator.join(v)

    separator = separator.rstrip(" ") + " "

    return separator.join(v[:-1]) + " " + copula + " " + v[-1]


INTERVALS = [
    ("years", 365),
    ("weeks", 7),
    ("days", 24),
    ("hours", 60),
    ("minutes", 60),
    ("seconds", 1000),
    ("milliseconds", 1000),
    ("microseconds", 1000),
    ("nanoseconds", 1),
]

SHORT_NAMES = {
    "years": "y",
    "weeks": "w",
    "days": "d",
    "hours": "h",
    "minutes": "m",
    "seconds": "s",
    "milliseconds": "ms",
    "microseconds": "µs",
    "nanoseconds": "ns",
}

cumprod = 1

for i in range(len(INTERVALS) - 1, -1, -1):
    name, value = INTERVALS[i]
    cumprod *= value
    INTERVALS[i] = (name, cumprod)


INTERVAL_CONVERSION = {t[0]: t[1] for t in INTERVALS}


def format_time_item(value: float, unit: str, short: bool = False) -> str:
    if short:
        unit = SHORT_NAMES[unit]

    if value == 0:
        return "0 %s" % unit

    if value < 1:
        return ("%.3f" % value).rstrip(".0") + " " + unit

    if not short and value == 1:
        unit = unit.rstrip("s")

    return "%i%s%s" % (value, "" if short else " ", unit)


def format_time_items(items: Iterable[Tuple[float, str]], short: bool = False):
    if short:
        return ", ".join(format_time_item(t[0], t[1], short=True) for t in items)
    else:
        return and_join(format_time_item(t[0], t[1]) for t in items)


def format_time(
    time: float,
    precision: str = "nanoseconds",
    unit: str = "nanoseconds",
    max_items: Optional[int] = None,
    short: bool = False,
) -> str:
    unit = unit.rstrip("s") + "s"
    precision = precision.rstrip("s") + "s"

    if time == 0:
        return format_time_item(0, unit, short=short)

    if unit != "nanoseconds":
        conversion = INTERVAL_CONVERSION.get(unit)

        if conversion is None:
            raise TypeError('invalid unit "%s"' % unit)

        time *= conversion

    if precision not in INTERVAL_CONVERSION:
        raise TypeError('invalid precision "%s"' % precision)

    result = []
    remain = 0

    for name, count in INTERVALS:
        value = time // count
        time -= value * count

        if name == precision:
            remain = time / count

        result.append((value, name))

    precised = []

    for t in result:
        if t[0]:
            precised.append(t)

        if t[1] == precision:
            break

    if not precised:
        return ("%.3f" % remain).rstrip(".0") + " " + unit

    if max_items is not None:
        precised = precised[:max_items]

    return format_time_items(precised, short=short)


format_seconds = partial(format_time, unit="seconds", precision="seconds")

AttributesSpec = Iterable[Union[str, Tuple[str, Any]]]


def obj_attr_iter(
    obj: Any, attributes: Optional[AttributesSpec] = None
) -> Iterator[Tuple[str, Any]]:
    # Given attributes
    if attributes is not None:
        for k in attributes:
            if isinstance(k, tuple):
                yield k[0], k[1]
            else:
                yield k, getattr(obj, k)

        return

    slots = getattr(obj, "__slots__", None)

    # Slots
    if slots is not None:
        for k in slots:
            if k.startswith("_"):
                continue

            yield k, getattr(obj, k)

        return

    # All attributes
    for k in sorted(dir(obj)):
        if k.startswith("_"):
            continue

        yield k, getattr(obj, k)


def format_repr(
    obj: Any,
    attributes: Optional[AttributesSpec] = None,
    conditionals: Optional[Container[str]] = None,
    max_length: Optional[int] = None,
    style: Optional[str] = "<>",
) -> str:
    if style != "<>" and style != "()":
        raise TypeError('style should be "<>" or "()"')

    class_name = obj.__class__.__name__

    parts = []

    for k, v in obj_attr_iter(obj, attributes):
        if conditionals is not None and k in conditionals and v is None:
            continue

        if max_length is not None and isinstance(v, str):
            v = v[: max(0, max_length - 1)] + "…"

        parts.append("{}={!r}".format(k, v))

    r = ""

    if style == "<>":
        r = "<" + class_name + " "
        r += " ".join(parts)
        r += ">"

    else:
        r = class_name + "("
        r += ", ".join(parts)
        r += ")"

    return r


FILESIZE_SUFFIXES = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
SHORT_FILESIZE_SUFFIXES = ["K", "M", "G", "T", "P", "E", "Z", "Y"]
FILESIZE_BINARY_SUFFIXES = [
    "KiB",
    "MiB",
    "GiB",
    "TiB",
    "PiB",
    "EiB",
    "ZiB",
    "YiB",
]


def format_filesize(
    size: int,
    *,
    binary: bool = False,
    precision: Optional[int] = 1,
    separator: Optional[str] = "",
    short: bool = False
) -> str:
    if size < 0:
        raise TypeError("expecting a number >= 0")

    suffixes = FILESIZE_BINARY_SUFFIXES if binary else FILESIZE_SUFFIXES

    if short:
        suffixes = SHORT_FILESIZE_SUFFIXES

    base = 1024 if binary else 1000

    if size < base:
        return "{:,}".format(size)

    suffix = None
    unit = None

    for i, suffix in enumerate(suffixes, 2):
        unit = base**i

        if size < unit:
            break

    assert suffix is not None and unit is not None

    return "{:,.{precision}f}{separator}{}".format(
        (base * size / unit),
        suffix,
        precision=precision,
        separator=separator,
    )
