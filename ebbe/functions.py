# =============================================================================
# Ebbe Functions
# =============================================================================
#


def with_prev(iterator):
    prev = None

    for item in iterator:
        if prev is not None:
            yield prev, item

        prev = item
