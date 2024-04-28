import hashlib

import pytest

from regidi import digest18, digest24


def test_digest18_single():
    digest = digest18(122775)

    assert digest == "potato"


def test_digest18_all():
    h = hashlib.sha256(usedforsecurity=False)
    for i in range(0, 2**18):
        digest = digest18(i)
        h.update(digest.encode())

    # Expected sha256 digest can be regenerated with: regidi --all | tr -d '\n' | sha256sum
    assert h.hexdigest() == "d41c3a064bf896a7e5667d6d11e14ac5d99f00d5d57810566a95b662e31fd3e5"


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
