# =============================================================================
# Ebbe Library Enpoint
# =============================================================================
#
from ebbe.benchmark import Timer
from ebbe.iter import (
    as_chunks,
    as_grams,
    fail_fast,
    uniq,
    distinct,
    with_prev,
    with_prev_and_next,
    with_next,
    with_is_first,
    with_is_last,
    without_first
)
from ebbe.format import (
    prettyprint_int,
    prettyprint_seconds
)
from ebbe.utils import (
    noop,
    get,
    getter,
    getpath,
    pathgetter,
    sorted_uniq,
    indexed,
    grouped,
    partitioned,
    grouped_items,
    partitioned_items
)
