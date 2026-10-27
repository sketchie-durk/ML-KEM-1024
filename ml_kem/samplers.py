
from .utils import shake256
from .params import ETA1, ETA2

def cbd(eta: int, seed_bytes: bytes):
    stream = shake256(seed_bytes, 256 * eta * 2 // 8 + 1)
    poly = []
    bit_idx = 0
    def get_bit():
        nonlocal bit_idx
        byte_idx = bit_idx // 8
        bit_offset = bit_idx % 8
        bit = (stream[byte_idx] >> bit_offset) & 1
        bit_idx += 1
        return bit
    for _ in range(256):
        a = sum(get_bit() for _ in range(eta))
        b = sum(get_bit() for _ in range(eta))
        poly.append(a - b)
    return poly
