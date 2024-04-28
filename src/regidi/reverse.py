from typing import Any, Generator, Literal

from . import digest18, lut, substitutions
from .utils import get_18bit_key, get_21bit_key

reverse_substitutions = {v: k for k, v in substitutions.items()}


def reverse_digest18(digest: str) -> int | None:
    """
    Finds the input that generates the given digest18 output - if there is one.

    Not all valid digests have a corresponding input;
    The digests with alternative syllables are used to substitute unwanted basic digests and not all of them are used.
    """
    if not (6 <= len(digest) <= 9):
        raise ValueError(f"Expected 6-9 characters, got {len(digest)}")

    for s1_len, s2_len, s3_len in get_possible_syllable_lengths(len(digest)):
        s1 = digest[:s1_len]
        s2 = digest[s1_len : s1_len + s2_len]
        s3 = digest[-s3_len:]

        if s1 in lut and s2 in lut and s3 in lut:
            break
    else:
        raise ValueError(f"Could not divide digest into syllables: {digest}")

    k1 = lut.index(s1)
    k2 = lut.index(s2)
    k3 = lut.index(s3)

    if k1 < 64 and k2 < 64 and k3 < 64:
        # Only basic syllables
        return get_18bit_key(k1, k2, k3)
    else:
        # Alternative syllables used; find reverse mapping from substitution
        lut_key = get_21bit_key(k1, k2, k3)

        return reverse_substitutions.get(lut_key, None)


def get_possible_syllable_lengths(
    digest_length: int,
) -> Generator[tuple[Literal[2, 3], Literal[2, 3], Literal[2, 3]], Any, None]:
    if digest_length == 9:
        yield 3, 3, 3
    elif digest_length == 8:
        yield 2, 3, 3
        yield 3, 2, 3
        yield 3, 3, 2
    elif digest_length == 7:
        yield 2, 2, 3
        yield 2, 3, 2
        yield 3, 2, 2
    elif digest_length == 6:
        yield 2, 2, 2
    else:
        raise ValueError(f"Invalid digest length: {digest_length}")


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description=reverse_digest18.__doc__)
    parser.add_argument("digest", help="Digest to try to reverse")
    parser.add_argument("-f", "--format", choices=["int", "hex"], default="hex", help="Output format")
    args = parser.parse_args()

    key = reverse_digest18(args.digest)
    if key is None:
        print("No input found for the given digest", file=sys.stderr)
        exit(1)

    assert digest18(key) == args.digest

    if args.format == "hex":
        print(hex(key))
    else:
        print(key)
