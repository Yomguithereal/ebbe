# =============================================================================
# Ebbe Formatting Unit Tests
# =============================================================================
from ebbe.format import format_int, and_join, format_time, format_seconds, format_repr


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

    def test_format_repr(self):
        class Video:
            name: str
            duration: int

            def __init__(self, name: str, duration: int):
                self.name = name
                self.duration = duration

        assert format_repr(Video("test", 45)) == "<Video duration=45 name='test'>"
        assert (
            format_repr(Video("test", 45), max_length=3)
            == "<Video duration=45 name='te…'>"
        )
        assert (
            format_repr(Video("test", 45), style="()")
            == "Video(duration=45, name='test')"
        )
        assert (
            format_repr(Video("test", 45), style="()", attributes=("duration",))
            == "Video(duration=45)"
        )

        class SlottedVideo:
            __slots__ = ("name", "age")

            def __init__(self, name: str, age: int):
                self.name = name
                self.age = age

        assert (
            format_repr(SlottedVideo("test", 34)) == "<SlottedVideo name='test' age=34>"
        )

        class OptionalVideo:
            def __init__(self, name, age=None):
                self.name = name
                self.age = age

        assert (
            format_repr(OptionalVideo("test")) == "<OptionalVideo age=None name='test'>"
        )

        assert (
            format_repr(OptionalVideo("test"), conditionals=("age",))
            == "<OptionalVideo name='test'>"
        )

        assert (
            format_repr(
                OptionalVideo("test"),
                attributes=["name", ("dtype", None), ("custom", True)],
                conditionals=("dtype",),
            )
            == "<OptionalVideo name='test' custom=True>"
        )
