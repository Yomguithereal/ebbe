# =============================================================================
# Ebbe Benchmark Helpers
# =============================================================================
#
import sys
from timeit import default_timer as timer

from ebbe.format import prettyprint_time


class Timer(object):
    def __init__(self, name="Timer", file=sys.stderr, unit="milliseconds"):
        self.name = name
        self.file = file
        self.unit = unit

    def __enter__(self):
        self.start = timer()

    def __exit__(self, *args):
        self.end = timer()
        self.duration = self.end - self.start
        print(
            "%s:" % self.name,
            prettyprint_time(self.duration, unit="milliseconds"),
            file=self.file,
        )
