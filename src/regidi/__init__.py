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
lut = [
    # 64 primary syllables
    "ba",   "cha",  "do",   "ka",   "ma",   "no",   "si",   "te",
    "be",   "che",  "fa",   "ki",   "me",   "nu",   "so",   "ti",
    "bi",   "chi",  "fi",   "ko",   "mi",   "pa",   "su",   "to",
    "bo",   "cho",  "fo",   "la",   "mo",   "po",   "spa",  "tu",
    "bro",  "chu",  "ga",   "le",   "mu",   "ra",   "sta",  "tra",
    "ca",   "da",   "gi",   "li",   "na",   "re",   "sti",  "tri",
    "co",   "de",   "go",   "lo",   "ne",   "ro",   "sto",  "tro",
    "cu",   "di",   "gra",  "lu",   "ni",   "sa",   "ta",   "tru",
    # 32 alternative syllables for substitutions
    "al",   "at",   "el",   "in",   "mac",  "up",   "cov",  "cra",
    "bu",   "bre",  "cro",  "du",   "fe",   "gu",   "gri",  "gru",
    "ku",   "pe",   "pu",   "ru",   "sla",  "slo",  "spe",  "spi",
    "spu",  "ste",  "stu",  "tre",  "fu",   "ce",   "ci",   "spy"
]
# fmt: on

substitutions = _load_substitutions()


def digest18(hash: int | bytes) -> str:
    """
    Generates an 18-bit digest consisting of three syllables.

    Uses the lowest 18 bits of the given input, where each syllable is based on 6 bits.

    Example: `potato`
    """
    mask = 0b111111_111111_111111  # 18 bits

    if isinstance(hash, bytes):
        key: int = int.from_bytes(hash, "big") & mask
    elif isinstance(hash, int):
        key: int = hash & mask
    else:
        raise TypeError("hash must be bytes or int")

    if key in substitutions:
        key = substitutions[key]
        k3 = key & 127
        k2 = (key >> 7) & 127
        k1 = (key >> 14) & 127
    else:
        k3 = key & 63
        k2 = (key >> 6) & 63
        k1 = (key >> 12) & 63

    return f"{lut[k1]}{lut[k2]}{lut[k3]}"


def digest24(hash: int | bytes) -> str:
    """
    Generates a 24-bit digest consisting of three syllables and two digits.

    Uses the lowest 24 bits of the given input.
    The syllables are generated from the lowest 18 bits in the exact same way as the digest18 function.
    The two digits are appended to the end based on the remaining 6 bits, in the range 01-64.

    Example: `potato38`
    """
    mask = 0b111111_111111_111111_111111  # 24 bits

    if isinstance(hash, bytes):
        key: int = int.from_bytes(hash, "big") & mask
    elif isinstance(hash, int):
        key: int = hash & mask
    else:
        raise TypeError("hash must be bytes or int")

    digits = ((key >> 18) & 63) + 1

    lut_key = key & 0b111111_111111_111111  # 18 bits
    if lut_key in substitutions:
        key = substitutions[lut_key]
        k3 = key & 127
        k2 = (key >> 7) & 127
        k1 = (key >> 14) & 127
    else:
        k3 = key & 63
        k2 = (key >> 6) & 63
        k1 = (key >> 12) & 63

    return f"{lut[k1]}{lut[k2]}{lut[k3]}{digits:02d}"
