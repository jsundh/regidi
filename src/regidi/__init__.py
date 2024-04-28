import warnings
from importlib.resources import files

substitutions_file = files() / "substitutions.txt"


def _load_substitutions() -> dict[int, int]:
    try:
        substitutions: dict[int, int] = {}
        with substitutions_file.open("r") as f:
            for line in (line.rstrip() for line in f):
                if not line:
                    continue

                key, value = line.strip().split(",")
                substitutions[int(key)] = int(value)

            return substitutions
    except Exception as e:
        warnings.warn(f"Failed to load substitutions: {e}. Using no substitutions.")
        return {}


# fmt: off
base6 = [
    "ba",   "cha",  "do",   "ka",   "ma",   "no",   "si",   "te",
    "be",   "che",  "fa",   "ki",   "me",   "nu",   "so",   "ti",
    "bi",   "chi",  "fi",   "ko",   "mi",   "pa",   "su",   "to",
    "bo",   "cho",  "fo",   "la",   "mo",   "po",   "spa",  "tu",
    "bro",  "chu",  "ga",   "le",   "mu",   "ra",   "sta",  "tra",
    "ca",   "da",   "gi",   "li",   "na",   "re",   "sti",  "tri",
    "co",   "de",   "go",   "lo",   "ne",   "ro",   "sto",  "tro",
    "cu",   "di",   "gra",  "lu",   "ni",   "sa",   "ta",   "tru"
]

aux5 = [
    "al",   "at",   "el",   "in",   "mac",  "up",   "cov",  "cra",
    "bu",   "bre",  "cro",  "du",   "fe",   "gu",   "gri",  "gru",
    "ku",   "pe",   "pu",   "su",   "sla",  "slo",  "spe",  "spi",
    "spu",  "ste",  "stu",  "tre",  "fu",   "ce",   "ci",   "spy"
]
# fmt: on

substitutions = _load_substitutions()


def digest18(hash: int | bytes) -> str:
    """
    Generates a three-syllable digest using the first (lowest) 18 bits of the given hash.
    """
    mask = 0b111111_111111_111111  # 18 bits

    if isinstance(hash, bytes):
        key: int = int.from_bytes(hash, "big") & mask
    elif isinstance(hash, int):
        key: int = hash & mask
    else:
        raise TypeError("hash must be bytes or int")

    if key in substitutions:
        lut = aux5
        key = substitutions[key]
    else:
        lut = base6

    k3 = key & 63
    k2 = (key >> 6) & 63
    k1 = (key >> 12) & 63

    return f"{lut[k1]}{lut[k2]}{lut[k3]}"


def digest24(hash: int | bytes) -> str:
    """
    Generates a ~24.63-bit digest using the first 25 bits of the given hash.

    The digest consists of the same three syllables as digest18 from the first 18 bits together
    with two digits in the range 01-99 appended to the end, extracted from the remaining 7 bits.

    Example: `potato38`
    """
    mask = 0b1111111_111111_111111_111111  # 25 bits

    if isinstance(hash, bytes):
        key: int = int.from_bytes(hash, "big") & mask
    elif isinstance(hash, int):
        key: int = hash & mask
    else:
        raise TypeError("hash must be bytes or int")

    digits = (key >> 18) % 99 + 1

    base6_key = key & 0b111111_111111_111111  # 18 bits
    if base6_key in substitutions:
        lut = aux5
        key = substitutions[base6_key]
    else:
        lut = base6

    k3 = key & 63
    k2 = (key >> 6) & 63
    k1 = (key >> 12) & 63

    return f"{lut[k1]}{lut[k2]}{lut[k3]}{digits:02d}"
