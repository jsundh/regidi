import pytest

from regidi import aux5, base6, digest18, digest24


def test_aux5_table():
    assert len(aux5) == 32
    assert sorted(aux5) == sorted(set(aux5))


def test_base6_table():
    assert len(base6) == 64
    assert sorted(aux5) == sorted(set(aux5))


def test_digest18():
    digest = digest18(122775)

    assert digest == "potato"


class TestDigest24:
    @pytest.mark.parametrize(["test_input", "expected_digits"], [(i << 18, f"{(i+1):02d}") for i in range(0, 99)])
    def test_digits(self, test_input, expected_digits):
        digest = digest24(test_input)  # type: ignore

        assert digest[-2:] == expected_digits

    def test_returns_same_syllables_as_digest18(self):
        input_hash = 63471  # No bits above 18 set => digits should be 01

        d18 = digest18(input_hash)
        d24 = digest24(input_hash)

        assert d24 == f"{d18}01"
