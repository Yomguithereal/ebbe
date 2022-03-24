# =============================================================================
# Ebbe Formatting Unit Tests
# =============================================================================
from ebbe.format import format_int, and_join, format_time, format_seconds


class TestDecorators(object):
    def test_format_int(self):
        assert format_int(4.0) == "4"
        assert format_int(400) == "400"
        assert format_int(4000) == "4,000"
        assert format_int(1_000_000) == "1,000,000"
        assert format_int(4000, separator=" ") == "4 000"

    def test_and_join(self):
        assert and_join([]) == ""
        assert and_join(["a"]) == "a"
        assert and_join(["a", "b"]) == "a and b"
        assert and_join(["a", "b", "c"]) == "a, b and c"
        assert (
            and_join(["a", "b", "c", "d"], copula="und", separator=";")
            == "a; b; c und d"
        )

    def test_format_time(self):
        assert format_time(57309) == "57 microseconds and 309 nanoseconds"
        assert format_time(57309, precision="microseconds") == "57 microseconds"
        assert (
            format_time(4865268458795)
            == "1 hour, 21 minutes, 5 seconds, 268 milliseconds, 458 microseconds and 795 nanoseconds"
        )
        assert (
            format_time(4865268458795, precision="minutes") == "1 hour and 21 minutes"
        )
        assert format_time(0.48680) == "0.487 nanoseconds"
        assert format_time(0.48000) == "0.48 nanoseconds"
        assert format_time(78, unit="seconds") == "1 minute and 18 seconds"
        assert (
            format_time(0.49704864, unit="seconds")
            == "497 milliseconds, 48 microseconds and 640 nanoseconds"
        )
        assert (
            format_time(0.49704864, unit="seconds", precision="milliseconds")
            == "497 milliseconds"
        )
        assert format_time(1.846, unit="seconds", precision="seconds") == "1 second"
        assert format_seconds(1974) == "32 minutes and 54 seconds"
        assert format_seconds(0.74508664) == "0.745 seconds"
        assert (
            format_time(0.74508664, unit="seconds", precision="milliseconds")
            == "745 milliseconds"
        )
        assert (
            format_time(0.00074508664, unit="seconds", precision="microseconds")
            == "745 microseconds"
        )
        assert format_time(0) == "0 nanoseconds"
        assert format_time(4865268458795, max_items=2) == "1 hour and 21 minutes"
        assert (
            format_time(4865268458795, short=True) == "1h, 21m, 5s, 268ms, 458µs, 795ns"
        )
