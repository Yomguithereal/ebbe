# =============================================================================
# Ebbe Library Enpoint
# =============================================================================
#
from ebbe.iter import (
    as_chunks,
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
from ebbe.utils import (
    noop,
    get,
    getter,
    getpath,
    pathgetter,
    sorted_uniq,
    indexed,
    grouped,
    partitioned
)
