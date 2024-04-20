# regidi

18-bit Readable Gibberish Digests to use when you want
a short, memorable representation of a hash function digest, UUID, or similar.

```python
>>> import regidi
>>> regidi.digest18(187065) # Accepts int or bytes
'regidi'
```

## Usage

**BYOH**: This library does not provide a hash function - bring your own if you want digests of arbitrary data.

