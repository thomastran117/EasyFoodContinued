import random

def is_positive_integer(s):
    return s.isdigit() and int(s) > 0


BASE_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(BASE_ALPHABET)
KEY = "mysecretkey123"


def get_shuffled_alphabet():
    """Generate a deterministic shuffled alphabet based on the key."""
    shuffled = list(BASE_ALPHABET)
    rng = random.Random(KEY)
    rng.shuffle(shuffled)
    return "".join(shuffled)


def encode_id(n):
    """Encodes an integer to a unique string using a key."""
    alphabet = get_shuffled_alphabet()
    if n == 0:
        return alphabet[0]
    s = []
    while n > 0:
        n, rem = divmod(n, BASE)
        s.append(alphabet[rem])
    return "".join(reversed(s))


def decode_id(s):
    """Decodes a string back to the original integer using a key."""
    alphabet = get_shuffled_alphabet()
    n = 0
    for char in s:
        n = n * BASE + alphabet.index(char)
    return n
