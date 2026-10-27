
N = 256
Q = 3329
K = 4
ETA1 = 2
ETA2 = 2
ZETA = 17

def get_bit_reversed_zetas():
    zetas = []
    for i in range(256):
        rev = 0
        temp = i
        for _ in range(8):
            rev = (rev << 1) | (temp & 1)
            temp >>= 1
        zetas.append(pow(ZETA, rev, Q))
    return zetas

ZETAS = get_bit_reversed_zetas()
