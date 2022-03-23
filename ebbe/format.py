# =============================================================================
# Ebbe Formatting Helpers
# =============================================================================
#
from functools import partial


def prettyprint_int(n, separator=","):
    s = "{:,}".format(int(n))

    if separator != ",":
        return s.replace(",", separator)

    return s


def and_join(v, separator=",", copula="and"):
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

cumprod = 1

for i in range(len(INTERVALS) - 1, -1, -1):
    name, value = INTERVALS[i]
    cumprod *= value
    INTERVALS[i] = (name, cumprod)


INTERVAL_CONVERSION = {t[0]: t[1] for t in INTERVALS}


def prettyprint_time(time, precision="nanoseconds", unit="nanoseconds"):
    unit = unit.rstrip("s") + "s"
    precision = precision.rstrip("s") + "s"

    if unit != "nanoseconds":
        conversion = INTERVAL_CONVERSION.get(unit)

        if conversion is None:
            raise TypeError('invalid unit "%s"' % unit)

        time *= conversion

    if precision not in INTERVAL_CONVERSION:
        raise TypeError('invalid precision "%s"' % precision)

    result = []

    for name, count in INTERVALS:
        value = time // count

        if value:
            time -= value * count

            formatted_name = name

            if value == 1:
                formatted_name = name.rstrip("s")

            result.append("%i %s" % (value, formatted_name))

        if name == unit:
            time /= count
            break

        elif name == precision:
            break

    if not result:
        return ("%.3f" % time).rstrip("0") + " " + unit

    return and_join(result)


prettyprint_seconds = partial(prettyprint_time, unit="seconds", precision="seconds")
