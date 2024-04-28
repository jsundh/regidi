"""
Print regidi digests for the given hex string or integer (base 10) inputs.

If no inputs are provided as arguments, read from stdin.
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
    parser.add_argument("-f", "--format", choices=["int", "hex"], default="hex", help="Input format")
    parser.add_argument(
        "-l", "--length", type=int, choices=[18, 24], default=18, help="Regidi digest length to generate"
    )
    parser.add_argument("input", nargs="*", help="Inputs to digest")
    args = parser.parse_args()

    input_src = args.input or sys.stdin
    digest_fn = digests[args.length]

    for line in input_src:
        base = 16 if args.format == "hex" else 10
        key = int(line.strip(), base)
        print(digest_fn(key))


if __name__ == "__main__":
    main()
