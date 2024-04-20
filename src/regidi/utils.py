import itertools
from typing import Generator

from . import aux5, base6


def get_key(k1: int, k2: int, k3: int):
    return k1 << 12 | k2 << 6 | k3


def generate_all_base6() -> Generator[tuple[int, str], None, None]:
    for k1, k2, k3 in itertools.product(range(len(base6)), repeat=3):
        yield get_key(k1, k2, k3), f"{base6[k1]}{base6[k2]}{base6[k3]}"


def generate_all_aux5() -> Generator[tuple[int, str], None, None]:
    # First eight entries in aux5 are only intended to be used as the first syllable in the digest
    general_start = 8
    end = len(aux5)
    for k1, k2, k3 in itertools.product(range(end), range(general_start, end), range(general_start, end)):
        yield get_key(k1, k2, k3), f"{aux5[k1]}{aux5[k2]}{aux5[k3]}"
