"""
Print regidi digests for the given hex string or integer (base 10) inputs.

If no inputs are provided as arguments, read from stdin.
"""

import argparse
import sys
from typing import Iterable, Literal

from . import digest18, digest24


def main():
    digests = {
        18: digest18,
        24: digest24,
    }

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--all", action="store_true", help="Print all digests")
    parser.add_argument("-f", "--format", choices=["int", "hex"], default="hex", help="Input format")
    parser.add_argument(
        "-l", "--length", type=int, choices=[18, 24], default=18, help="Regidi digest length to generate"
    )
    parser.add_argument("input", nargs="*", help="Inputs to digest")
    args = parser.parse_args()

    if args.all:
        input_src = range(2**args.length)
    elif args.input and args.input[0] != "-":
        input_src = _preprocess_inputs(args.input, args.format)
    else:
        input_src = _preprocess_inputs(sys.stdin, args.format)

    digest_fn = digests[args.length]

    for key in input_src:
        print(digest_fn(key))


def _preprocess_inputs(inputs: Iterable[str], format: Literal["hex", "int"]) -> Iterable[int]:
    base = 16 if format == "hex" else 10

    return (int(str_key, base) for i in inputs if (str_key := i.strip()) != "")


if __name__ == "__main__":
    main()
