# =============================================================================
# Ebbe Benchmark Helpers
# =============================================================================
#
import sys
from timeit import default_timer as timer

from ebbe.format import prettyprint_seconds


class Timer(object):
    def __init__(self, name="Timer", file=sys.stderr):
        self.name = name
        self.file = file

    def __enter__(self):
        self.start = timer()

    def __exit__(self, *args):
        self.end = timer()
        self.duration = self.end - self.start
        print("%s:" % self.name, prettyprint_seconds(self.duration), file=self.file)
