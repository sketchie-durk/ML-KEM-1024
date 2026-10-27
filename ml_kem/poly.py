
from typing import List
from .params import N, Q, ZETAS

Polynomial = List[int]

def ntt(a: Polynomial) -> Polynomial:
    a = list(a)
    k = 1
    for length in [128, 64, 32, 16, 8, 4, 2, 1]:
        for start in range(0, N, 2 * length):
            zeta = ZETAS[k]
            k += 1
            for j in range(start, start + length):
                t = (zeta * a[j + length]) % Q
                a[j + length] = (a[j] - t) % Q
                a[j] = (a[j] + t) % Q
    return a

def inv_ntt(a: Polynomial) -> Polynomial:
    a = list(a)
    k = 127
    for length in [1, 2, 4, 8, 16, 32, 64, 128]:
        for start in range(0, N, 2 * length):
            zeta = ZETAS[k]
            k -= 1
            for j in range(start, start + length):
                t = a[j]
                a[j] = (t + a[j + length]) % Q
                a[j + length] = (zeta * (a[j + length] - t)) % Q
    n_inv = pow(N, Q - 2, Q)
    return [(val * n_inv) % Q for val in a]

def poly_add(a: Polynomial, b: Polynomial) -> Polynomial:
    return [(a[i] + b[i]) % Q for i in range(N)]

def poly_sub(a: Polynomial, b: Polynomial) -> Polynomial:
    return [(a[i] - b[i]) % Q for i in range(N)]

def poly_mul_ntt(a_ntt: Polynomial, b_ntt: Polynomial) -> Polynomial:
    return [(a_ntt[i] * b_ntt[i]) % Q for i in range(N)]
