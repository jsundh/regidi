"""
Print regidi digests for the given hex strings.

If no hex strings are provided as arguments, read from stdin.
"""

import argparse
import sys

from . import digest18, digest24


def main():
    digests = {
        18: digest18,
        24: digest24,
    }

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-l", "--length", type=int, choices=[18, 24], default=18, help="Regidi digest length to generate"
    )
    parser.add_argument("hash", nargs="*", help="Hex strings to digest")
    args = parser.parse_args()

    input_src = args.hash or sys.stdin
    digest_fn = digests[args.length]

    for line in input_src:
        h = int(line.strip(), 16)
        print(digest_fn(h))


if __name__ == "__main__":
    main()
