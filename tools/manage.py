#!/usr/bin/env python3
from enum import StrEnum
from pathlib import Path

import typer
from tqdm import tqdm

from regidi import digest18, substitutions_file
from regidi.utils import generate_all_aux5, generate_all_base6

AUX5_SIZE = 32 * (32 - 8) * (32 - 8)
BASE6_SIZE = 2**18


class LookupTable(StrEnum):
    BASE6 = "base6"
    AUX5 = "aux5"


app = typer.Typer()


def load_bad_words() -> list[str]:
    path = Path(__file__).parent / "bad-words.txt"
    return [word for word in path.read_text().splitlines() if word != ""]


@app.command()
def find_bad_words(table: LookupTable):
    """
    Finds bad words in all possible digests of the given table.
    """
    match table:
        case LookupTable.BASE6:
            digests = generate_all_base6()
            total = BASE6_SIZE
        case LookupTable.AUX5:
            digests = generate_all_aux5()
            total = AUX5_SIZE

    bad_words = load_bad_words()

    excludes = 0
    matches = set()
    for _, digest in tqdm(digests, total=total):
        for bad_word in bad_words:
            if bad_word in digest:
                excludes += 1
                matches.add(bad_word)
                break

    print(f"Bad words matched ({len(matches)}): ")
    print(*sorted(matches), sep=", ")
    print(f"Digests that would be excluded: {excludes}/{total} ({excludes / total:.2%})")


@app.command()
def update_substitutions():
    """
    Updates the substitution resource files based on the current bad-words.txt.
    """
    bad_words = load_bad_words()

    def generate_allowed_aux5():
        for key, digest in tqdm(generate_all_aux5(), total=AUX5_SIZE, desc="aux5", colour="red"):
            if not any(bad_word in digest for bad_word in bad_words):
                yield key

    aux_keys = generate_allowed_aux5()

    base_to_aux = {}
    for key, digest in tqdm(generate_all_base6(), total=BASE6_SIZE, desc="base6", colour="blue"):
        if any(bad_word in digest for bad_word in bad_words):
            aux_key = next(aux_keys)
            base_to_aux[key] = aux_key

    with Path(str(substitutions_file)).open("w") as f:
        for base_key, aux_key in base_to_aux.items():
            f.write(f"{base_key},{aux_key}\n")


@app.command()
def validate_substitutions():
    """
    Checks that digest18 does not contain any bad words.
    """
    bad_words = load_bad_words()

    for i in tqdm(range(BASE6_SIZE)):
        digest = digest18(i)
        for bad_word in bad_words:
            if bad_word in digest:
                tqdm.write(f"Bad word '{bad_word}' found in {digest}, key={i}")
                tqdm.write("Run manage.py update-substitutions")
                return


if __name__ == "__main__":
    app()
