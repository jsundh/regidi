from regidi import digest18
from regidi.reverse import reverse_digest18


def test_reverse_digest18():
    for key in range(2**18):
        digest = digest18(key)
        reversed = reverse_digest18(digest)
        assert reversed == key, f"Failed for digest: {digest} -> {key}"
