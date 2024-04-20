# fmt: off
lut = [
    "ba",   "cha",  "do",   "ka",   "ma",   "no",   "si",   "te",
    "be",   "che",  "fa",   "ki",   "me",   "nu",   "so",   "ti",
    "bi",   "chi",  "fi",   "ko",   "mi",   "pa",   "su",   "to",
    "bo",   "cho",  "fo",   "la",   "mo",   "po",   "spa",  "tu",
    "bro",  "chu",  "ga",   "le",   "mu",   "ra",   "sta",  "tra",
    "ca",   "da",   "gi",   "li",   "na",   "re",   "sti",  "tri",
    "co",   "de",   "go",   "lo",   "ne",   "ro",   "sto",  "tro",
    "cu",   "di",   "gra",  "lu",   "ni",   "sa",   "ta",   "tru"
]
# fmt: on



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

    k3 = key & 63
    k2 = (key >> 6) & 63
    k1 = (key >> 12) & 63

    return f"{lut[k1]}{lut[k2]}{lut[k3]}"
