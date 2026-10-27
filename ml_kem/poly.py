
from typing import List
from .params import N, Q, ZETAS

Polynomial = List[int]

def ntt(a: Polynomial) -> Polynomial:
    a = list(a)
    k = 1
    len_ = 128
    while len_ >= 1:
        for start in range(0, N, 2 * len_):
            zeta = ZETAS[k]
            k += 1
            for j in range(start, start + len_):
                t = (zeta * a[j + len_]) % Q
                a[j + len_] = (a[j] - t) % Q
                a[j] = (a[j] + t) % Q
        len_ //= 2
    return a

def inv_ntt(a: Polynomial) -> Polynomial:
    a = list(a)
    k = 127
    len_ = 1
    while len_ <= 128:
        for start in range(0, N, 2 * len_):
            zeta = ZETAS[k]
            k -= 1
            for j in range(start, start + len_):
                t = a[j]
                a[j] = (t + a[j + len_]) % Q
                a[j + len_] = (zeta * (a[j + len_] - t)) % Q
        len_ *= 2
    n_inv = pow(N, Q - 2, Q)
    return [(val * n_inv) % Q for val in a]

def poly_add(a: Polynomial, b: Polynomial) -> Polynomial:
    return [(a[i] + b[i]) % Q for i in range(N)]

def poly_sub(a: Polynomial, b: Polynomial) -> Polynomial:
    return [(a[i] - b[i]) % Q for i in range(N)]

def poly_mul_ntt(a_ntt: Polynomial, b_ntt: Polynomial) -> Polynomial:
    return [(a_ntt[i] * b_ntt[i]) % Q for i in range(N)]
