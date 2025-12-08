import math
import random
import time
from typing import Tuple

from sympy import randprime


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def mod_inverse(a: int, m: int) -> int:
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def generate_large_prime(bits: int) -> int:
    if bits < 2:
        raise ValueError("bits must be >= 2")
    # randprime(low, high) returns a random prime in [low, high)
    low = 1 << (bits - 1)
    high = 1 << bits
    return int(randprime(low, high))


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def generate_rsa_keys(bits: int):
    if bits < 16:
        raise ValueError("RSA key bits should be >= 16 for this demo")
    half = bits // 2
    p = generate_large_prime(half)
    q = generate_large_prime(bits - half)
    while p == q:
        q = generate_large_prime(bits - half)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    # Ensure e and phi are coprime; if not, regenerate primes (rare)
    if gcd(e, phi) != 1:
        return generate_rsa_keys(bits)
    d = mod_inverse(e, phi)
    public_key = (n, e)
    private_key = (n, d, p, q)
    return public_key, private_key


def rsa_encrypt(message: int, public_key: Tuple[int, int]) -> int:
    n, e = public_key
    if message >= n:
        raise ValueError("Message integer too large for modulus n")
    return pow(message, e, n)


def rsa_decrypt(ciphertext: int, private_key) -> int:
    # private_key can be (n, d) or (n, d, p, q)
    if len(private_key) < 2:
        raise ValueError("private_key must contain at least (n, d)")
    n, d = private_key[0], private_key[1]
    return pow(ciphertext, d, n)


def pollard_rho_function(x: int, c: int, n: int) -> int:
    return (pow(x, 2, n) + c) % n


def pollard_rho_single(n: int, c: int, x0: int, max_iter: int) -> int:
    x = x0
    y = x0
    d = 1
    for _ in range(max_iter):
        if d == n:
            return 1  # failure indicator to trigger retry in outer driver
        x = pollard_rho_function(x, c, n)
        y = pollard_rho_function(pollard_rho_function(y, c, n), c, n)
        d = gcd(abs(x - y), n)
        if 1 < d < n:
            return d
    return 1


def pollard_rho_factor(n: int, max_time_seconds: float = 20.0):
    # Handle trivial cases
    if n % 2 == 0:
        return 2, n // 2
    if n <= 3:
        return 1, n

    start = time.time()
    # Try multiple random parameters until timeout
    while time.time() - start < max_time_seconds:
        c = random.randrange(1, n)
        x0 = random.randrange(2, n - 1)
        # Increase iterations progressively within time budget
        for max_iter in (1000, 5000, 20000, 100000):
            if time.time() - start >= max_time_seconds:
                break
            d = pollard_rho_single(n, c, x0, max_iter)
            if 1 < d < n:
                p = d
                q = n // d
                if p * q == n:
                    if p > q:
                        p, q = q, p
                    return p, q
    return 1, n  # indicate failure by returning a trivial factor


def str_to_int(message: str) -> int:
    data = message.encode("utf-8")
    return int.from_bytes(data, byteorder="big")


def int_to_str(value: int) -> str:
    # compute minimal byte length
    length = (value.bit_length() + 7) // 8
    if length == 0:
        return ""
    data = value.to_bytes(length, byteorder="big")
    return data.decode("utf-8", errors="ignore")


def max_plaintext_bytes(n: int) -> int:
    # We avoid equality to n; using floor((log2(n)-1)/8)
    return max(1, (n.bit_length() - 1) // 8)


def split_message_to_int_blocks(message: str, n: int) -> list[int]:
    data = message.encode("utf-8")
    block_size = max_plaintext_bytes(n)
    blocks = []
    for i in range(0, len(data), block_size):
        chunk = data[i:i + block_size]
        blocks.append(int.from_bytes(chunk, byteorder="big"))
    if not blocks:
        blocks = [0]
    return blocks


def join_int_blocks_to_message(blocks: list[int]) -> str:
    parts = []
    for v in blocks:
        if v == 0:
            parts.append(b"")
            continue
        length = (v.bit_length() + 7) // 8
        parts.append(v.to_bytes(length, byteorder="big"))
    try:
        return b"".join(parts).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def encrypt_message_to_blocks(message: str, public_key: Tuple[int, int]) -> list[int]:
    n, e = public_key
    m_blocks = split_message_to_int_blocks(message, n)
    return [pow(m, e, n) for m in m_blocks]


def decrypt_blocks_to_message(cipher_blocks: list[int], private_key) -> str:
    if len(private_key) < 2:
        raise ValueError("private_key must contain at least (n, d)")
    n, d = private_key[0], private_key[1]
    m_blocks = [pow(c, d, n) for c in cipher_blocks]
    return join_int_blocks_to_message(m_blocks)


