# =============================================================================
# Ebbe Formatting Helpers
# =============================================================================
#


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

INTERVAL_PRECISION = {n: len(INTERVALS) - i for i, n in enumerate(INTERVALS)}


def prettyprint_nanoseconds(nanoseconds, precision=None):
    clamp = None

    if precision is not None:
        clamp = INTERVAL_PRECISION.get(precision)

        if clamp is None:
            raise TypeError('invalid precision "%s"' % precision)

    result = []

    for name, count in INTERVALS:
        value = nanoseconds // count

        if value:
            nanoseconds -= value * count

            if value == 1:
                name = name.rstrip("s")

            result.append("%i %s" % (value, name))

    if not result:
        return "%.3f nanoseconds" % nanoseconds

    if clamp is not None:
        result = result[:clamp]

    return and_join(result)
