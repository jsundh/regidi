import itertools
from typing import Generator

from . import lut


def generate_all_basic() -> Generator[tuple[int, str], None, None]:
    for k1, k2, k3 in itertools.product(range(64), repeat=3):
        yield get_18bit_key(k1, k2, k3), f"{lut[k1]}{lut[k2]}{lut[k3]}"


def generate_all_substitutions() -> Generator[tuple[int, str], None, None]:
    # First eight alternative syllables are only intended to be used as the first syllable in the digest
    r1 = range(64, len(lut))
    r2 = range(64 + 8, len(lut))
    r3 = range(64 + 8, len(lut))
    for k1, k2, k3 in itertools.product(r1, r2, r3):
        yield get_21bit_key(k1, k2, k3), f"{lut[k1]}{lut[k2]}{lut[k3]}"


def get_18bit_key(k1: int, k2: int, k3: int):
    return k1 << 12 | k2 << 6 | k3


def get_21bit_key(k1: int, k2: int, k3: int):
    return k1 << 14 | k2 << 7 | k3
