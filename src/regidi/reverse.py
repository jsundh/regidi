from . import aux5, aux5_mapping, base6, digest18
from .utils import get_key


def reverse_digest18(digest: str) -> int | None:
    """
    Finds the input that generates the given digest18 output - if there is one.

    Not all valid digests have a corresponding input;
    The digests defined by the aux5 table are used to substitute unwanted base6 digests and not all of them are used.
    """
    if not (6 <= len(digest) <= 9):
        raise ValueError(f"Expected 6-9 characters, got {len(digest)}")

    if digest[:2] in aux5:
        lut = aux5
        lut_name = "aux5"
        s1, s2s3 = digest[:2], digest[2:]
    elif digest[:3] in aux5:
        lut = aux5
        lut_name = "aux5"
        s1, s2s3 = digest[:3], digest[3:]
    elif digest[:2] in base6:
        lut = base6
        lut_name = "base6"
        s1, s2s3 = digest[:2], digest[2:]
    elif digest[:3] in base6:
        lut = base6
        lut_name = "base6"
        s1, s2s3 = digest[:3], digest[3:]
    else:
        raise ValueError(f"First syllable not found in either base6 or aux5 lookup tables: {digest}")

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
        raise ValueError(f"Second syllable not found in lookup table {lut_name}: {s2}")
    if s3 not in lut:
        raise ValueError(f"Third syllable not found in lookup table {lut_name}: {s3}")

    k1 = lut.index(s1)
    k2 = lut.index(s2)
    k3 = lut.index(s3)

    lut_key = get_key(k1, k2, k3)

    if lut is base6:
        return lut_key

    # Find reverse mapping from aux5 to base6
    return next((base6_key for base6_key, aux_key in aux5_mapping.items() if aux_key == lut_key), None)


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
