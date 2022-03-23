# =============================================================================
# Ebbe Formatting Helpers
# =============================================================================
#


def prettyprint_int(n):
    return '{:,}'.format(int(n))


INTERVALS = [
    ('weeks', 60 * 60 * 24 * 7),  # 60 * 60 * 24 * 7
    ('days', 60 * 60 * 24),    # 60 * 60 * 24
    ('hours', 60 * 60),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1)
]


def prettyprint_seconds(seconds, granularity=None):
    result = []

    for name, count in INTERVALS:
        value = seconds // count

        if value:
            seconds -= value * count

            if value == 1:
                name = name.rstrip('s')

            result.append('%i %s' % (value, name))

    if not result:
        return '%.2f seconds' % seconds

    if granularity is not None:
        result = result[:granularity]

    return ', '.join(result)
