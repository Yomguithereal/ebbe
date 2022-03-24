# =============================================================================
# Ebbe Formatting Helpers
# =============================================================================
#
from typing import Iterable, Optional, Tuple
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
