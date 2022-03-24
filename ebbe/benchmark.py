# =============================================================================
# Ebbe Benchmark Helpers
# =============================================================================
#
import sys
from timeit import default_timer as timer
from typing import TextIO

from ebbe.format import format_time


class Timer(object):
    def __init__(
        self,
        name: str = "Timer",
        file: TextIO = sys.stderr,
        precision: str = "nanoseconds",
    ):
        self.name = name
        self.file = file
        self.precision = precision

    def __enter__(self):
        self.start = timer()

    def __exit__(self, *args):
        self.end = timer()
        self.duration = self.end - self.start
        print(
            "%s:" % self.name,
            format_time(
                self.duration,
                precision=self.precision,
                unit="seconds",
                max_items=2,
                short=True,
            ),
            file=self.file,
        )
