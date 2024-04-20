import csv
import warnings
from importlib.resources import files
from typing import NamedTuple

from bitarray import bitarray

base6_blocklist_path = files() / "base6-blocklist.bin"
aux5_mapping_path = files() / "aux5-mapping.csv"


class SubstitutionBasis(NamedTuple):
    base6_blocklist: bitarray
    aux5_mapping: dict[int, int]


def load_substitution_basis() -> SubstitutionBasis:
    base6_blocklist = bitarray()
    aux5_mapping: dict[int, int] = {}

    try:
        with base6_blocklist_path.open("rb") as f:
            base6_blocklist.fromfile(f)  # type: ignore

        with aux5_mapping_path.open("r") as f:
            reader = csv.reader(f, dialect=CsvDialect)
            for base6_key, aux5_key in reader:
                aux5_mapping[int(base6_key)] = int(aux5_key)

        return SubstitutionBasis(base6_blocklist, aux5_mapping)
    except Exception as e:
        warnings.warn(f"Failed to load substitution basis: {e}. Using empty blocklist.")

        return SubstitutionBasis(bitarray(2**18), {})


class CsvDialect(csv.Dialect):
    delimiter = ","
    skipinitialspace = False
    lineterminator = "\n"
    quoting = csv.QUOTE_NONE
