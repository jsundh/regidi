import hashlib

import pytest

from regidi import digest18, digest24, lut


def test_lut_table():
    assert len(lut) == 64 + 32
    assert sorted(lut) == sorted(set(lut))


def test_digest18_single():
    digest = digest18(122775)

    assert digest == "potato"


def test_digest18_unique():
    n = 2**18
    digests = set()
    for i in range(n):
        digest = digest18(i)
        digests.add(digest)

    assert len(digests) == n


def test_digest18_all():
    h = hashlib.sha256(usedforsecurity=False)
    for i in range(2**18):
        digest = digest18(i)
        h.update(digest.encode())

    # Expected sha256 digest can be regenerated with: regidi --all | tr -d '\n' | sha256sum
    assert h.hexdigest() == "9deeaa65c6a9b983385c23a2ff6b7b9cecfbcfda39352ade69a368091d1f991f"


class TestDigest24:
    @pytest.mark.parametrize(["test_input", "expected_digits"], [(i << 18, f"{(i+1):02d}") for i in range(0, 64)])
    def test_digits(self, test_input, expected_digits):
        digest = digest24(test_input)  # type: ignore

        assert digest[-2:] == expected_digits

    def test_returns_same_syllables_as_digest18(self):
        input_hash = 63471  # No bits above 18 set => digits should be 01

        d18 = digest18(input_hash)
        d24 = digest24(input_hash)

        assert d24 == f"{d18}01"
