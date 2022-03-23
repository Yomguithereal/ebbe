# =============================================================================
# Ebbe Formatting Unit Tests
# =============================================================================
from ebbe.format import prettyprint_int, and_join, prettyprint_nanoseconds


class TestDecorators(object):
    def test_prettyprint_int(self):
        assert prettyprint_int(4.0) == "4"
        assert prettyprint_int(400) == "400"
        assert prettyprint_int(4000) == "4,000"
        assert prettyprint_int(1_000_000) == "1,000,000"
        assert prettyprint_int(4000, separator=" ") == "4 000"

    def test_and_join(self):
        assert and_join([]) == ""
        assert and_join(["a"]) == "a"
        assert and_join(["a", "b"]) == "a and b"
        assert and_join(["a", "b", "c"]) == "a, b and c"
        assert (
            and_join(["a", "b", "c", "d"], copula="und", separator=";")
            == "a; b; c und d"
        )

    def test_prettyprint_nanoseconds(self):
        assert prettyprint_nanoseconds(57309) == "57 microseconds and 309 nanoseconds"
        assert (
            prettyprint_nanoseconds(4865268458795)
            == "1 hour, 21 minutes, 5 seconds, 268 milliseconds, 458 microseconds and 795 nanoseconds"
        )
        assert prettyprint_nanoseconds(0.48680) == "0.487 nanoseconds"
