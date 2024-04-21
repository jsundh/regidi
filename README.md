# regidi

18-bit or 24-bit Readable Gibberish Digests to use when you want
a short, memorable representation of a hash function digest, UUID, or similar.

```python
>>> import regidi
>>> regidi.digest18(187065) # Accepts int or bytes
'regidi'
```

## Installation

Regidi is available on <https://pypi.org/> and can be installed using pip:

```sh
pip install regidi
```

## Usage

**BYOH**: This library does not provide a hash function - bring your own if you want digests of arbitrary data.

The digest functions accepts either an `int` or `bytes` object as input. This matches the output of for instance both the functions in the built-in
[hashlib](https://docs.python.org/3/library/hashlib.html),
and the MurmurHash extension [mmh3](https://github.com/hajimes/mmh3).

### digest18

18-bit digest consisting of three syllables.

```python
import hashlib
import regidi

digest = regidi.digest18(hashlib.sha1(b"1234567890").digest())
assert digest == "kagrafo"
```

Constructs the digest using the lowest 18 bits in the input.

### digest24

24.63-bit digest with the same three syllables as `digest18` together with two digits at the end, 01-99 (~6.63 bits).

```python
import mmh3
import regidi

digest = regidi.digest24(mmh3.hash("regidi"))
assert digest == "raleca02"
```

If the input is smaller than $2^{18}$, `digest24` will generate the same digest as `digest18` with the digits `01`:

```python
import regidi

d18 = regidi.digest18(0)
d24 = regidi.digest24(0)

assert d24 == f"{d18}01"
```

### CLI

Installing the package also installs a CLI script to generate digests. Run with the `--help` flag for more information:

```sh
regidi --help
```

### Sanitized output

All theoretical digest outputs based on the initial set of syllables are checked against a list of bad words. Digests that contain any of the bad words are then substituted so that no digests contain any of the bad words on the list, while still retaining the 18-bit output. See [tools/README.md](./tools/README.md#bad-wordstxt) for more information.

## Development

This project uses [PDM](https://pdm-project.org/en/latest/).

### Updating bad-words.txt

The file [bad-words.txt](./tools/bad-words.txt) is not included in the distributed package.
Instead, the `regidi.substitution` package contains automatically generated resource files
that determine how syllable substitution should be performed to avoid bad words in digests.

If `bad-words.txt` is updated, these resource files have to be updated as well by running:

```
tools/manage.py update-substitution-data
```

**Note**: Changing the list of bad words also (very likely) changes the digest for inputs that require substitution.  
This means that currently the digest functions are not guaranteed to produce the same output between versions if the `bad-words.txt` file has been updated.
