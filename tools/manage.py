#!/usr/bin/env python3
from enum import StrEnum
from pathlib import Path

import typer
from tqdm import tqdm

from regidi import digest18, substitutions_file
from regidi.utils import generate_all_basic, generate_all_substitutions

BASIC_SIZE = 2**18
SUB_SIZE = 32 * (32 - 8) * (32 - 8)


class DigestSet(StrEnum):
    BASIC = "basic"
    SUB = "sub"


app = typer.Typer()
sub_app = typer.Typer()
app.add_typer(sub_app, name="substitutions")


def load_bad_words() -> list[str]:
    path = Path(__file__).parent / "bad-words.txt"
    return [word for word in path.read_text().splitlines() if word != ""]


@app.command()
def find_bad_words(digest_set: DigestSet):
    """
    Finds bad words in all possible digests of the given set.
    """
    match digest_set:
        case DigestSet.BASIC:
            digests = generate_all_basic()
            total = BASIC_SIZE
        case DigestSet.SUB:
            digests = generate_all_substitutions()
            total = SUB_SIZE

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


@sub_app.command("update")
def substitutions_update():
    """
    Updates the substitution resource files based on the current bad-words.txt.
    """
    bad_words = load_bad_words()

    def generate_allowed_substitutions():
        for key, digest in tqdm(generate_all_substitutions(), total=SUB_SIZE, desc="sub", colour="red"):
            if not any(bad_word in digest for bad_word in bad_words):
                yield key

    substitution_keys = generate_allowed_substitutions()

    basic_to_sub = {}
    for basic_key, digest in tqdm(generate_all_basic(), total=BASIC_SIZE, desc="basic", colour="blue"):
        if any(bad_word in digest for bad_word in bad_words):
            sub_key = next(substitution_keys)
            basic_to_sub[basic_key] = sub_key

    with Path(str(substitutions_file)).open("w") as f:
        for basic_key, sub_key in basic_to_sub.items():
            f.write(f"{basic_key},{sub_key}\n")


@sub_app.command("validate")
def substitutions_validate():
    """
    Checks that digest18 does not contain any bad words.
    """
    bad_words = load_bad_words()

    for i in tqdm(range(BASIC_SIZE)):
        digest = digest18(i)
        for bad_word in bad_words:
            if bad_word in digest:
                tqdm.write(f"Bad word '{bad_word}' found in {digest}, key={i}")
                tqdm.write("Run manage.py substitutions update")
                return


if __name__ == "__main__":
    app()
