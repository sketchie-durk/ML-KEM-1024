
import hashlib
from typing import List

def shake256(data: bytes, length: int) -> bytes:
    return hashlib.shake_256(data).digest(length)

def sha3_256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()

def sha3_512(data: bytes) -> bytes:
    return hashlib.sha3_512(data).digest()
