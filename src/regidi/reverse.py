from . import digest18, lut, substitutions
from .utils import get_18bit_key, get_21bit_key


def reverse_digest18(digest: str) -> int | None:
    """
    Finds the input that generates the given digest18 output - if there is one.

    Not all valid digests have a corresponding input;
    The digests with alternative syllables are used to substitute unwanted basic digests and not all of them are used.
    """
    if not (6 <= len(digest) <= 9):
        raise ValueError(f"Expected 6-9 characters, got {len(digest)}")

    if digest[:3] in lut:
        s1, s2s3 = digest[:3], digest[3:]
    elif digest[:2] in lut:
        s1, s2s3 = digest[:2], digest[2:]
    else:
        raise ValueError(f"First syllable not found in lookup table: {digest}")

    # A valid second syllable always ends in a vowel
    if s2s3[1] in "aeiou":
        s2 = s2s3[:2]
        s3 = s2s3[2:]
    elif s2s3[2] in "aeiou":
        s2 = s2s3[:3]
        s3 = s2s3[3:]
    else:
        raise ValueError(f"Could not find a valid second syllable in {digest}")

    if s2 not in lut:
        raise ValueError(f"Second syllable not found in lookup table: {s2}")
    if s3 not in lut:
        raise ValueError(f"Third syllable not found in lookup table: {s3}")

    k1 = lut.index(s1)
    k2 = lut.index(s2)
    k3 = lut.index(s3)

    if k1 < 64 and k2 < 64 and k3 < 64:
        # Only basic syllables
        return get_18bit_key(k1, k2, k3)
    else:
        # Alternative syllables used; find reverse mapping from substitution
        lut_key = get_21bit_key(k1, k2, k3)

        return next((basic_key for basic_key, sub_key in substitutions.items() if sub_key == lut_key), None)


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
