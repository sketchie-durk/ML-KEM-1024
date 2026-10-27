
import os
from .params import N, Q, K
from .poly import ntt, inv_ntt, poly_add, poly_sub, poly_mul_ntt
from .samplers import cbd
from .utils import sha3_256, shake256

class MLKEM1024:
    def __init__(self):
        self.k = K

    def _expand_a(self, seed: bytes):
        A = []
        for i in range(self.k):
            row = []
            for j in range(self.k):
                poly_seed = seed + i.to_bytes(1, 'big') + j.to_bytes(1, 'big')
                poly = [int.from_bytes(shake256(poly_seed, 2).replace(b'\x00', b'\x01'), 'little') % Q for _ in range(N)]
                row.append(poly)
            A.append(row)
        return A

    def keygen(self):
        d = os.urandom(32)
        A = self._expand_a(d)
        s = [cbd(2, d + b's' + i.to_bytes(1, 'big')) for i in range(self.k)]
        e = [cbd(2, d + b'e' + i.to_bytes(1, 'big')) for i in range(self.k)]
        s_ntt = [ntt(p) for p in s]
        e_ntt = [ntt(p) for p in e]
        t_ntt = []
        for i in range(self.k):
            row_sum = [0] * N
            for j in range(self.k):
                prod = poly_mul_ntt(A[i][j], s_ntt[j])
                row_sum = poly_add(row_sum, prod)
            t_ntt.append(poly_add(row_sum, e_ntt[i]))
        return (t_ntt, A), s_ntt

    def encaps(self, pk):
        t_ntt, A = pk
        m = os.urandom(32)
        r_seed = sha3_256(m + b"seed")
        r = [cbd(2, r_seed + i.to_bytes(1, 'big')) for i in range(self.k)]
        e1 = [cbd(2, r_seed + b'e1' + i.to_bytes(1, 'big')) for i in range(self.k)]
        e2 = cbd(2, r_seed + b'e2')
        r_ntt = [ntt(p) for p in r]
        u_ntt = []
        for i in range(self.k):
            row_sum = [0] * N
            for j in range(self.k):
                prod = poly_mul_ntt(A[i][j], r_ntt[j])
                row_sum = poly_add(row_sum, prod)
            u_ntt.append(poly_add(row_sum, ntt(e1[i])))
        v_ntt_sum = [0] * N
        for i in range(self.k):
            prod = poly_mul_ntt(t_ntt[i], r_ntt[i])
            v_ntt_sum = poly_add(v_ntt_sum, prod)
        v = poly_add(inv_ntt(v_ntt_sum), e2)
        m_bits = []
        for byte in m:
            for i in range(8): m_bits.append((byte >> i) & 1)
        for i in range(min(len(m_bits), N)):
            v[i] = (v[i] + m_bits[i] * (Q // 2)) % Q
        return (u_ntt, v), sha3_256(m)

    def decaps(self, ct, sk):
        u_ntt, v = ct
        s_ntt = sk
        inner_prod_ntt = [0] * N
        for i in range(self.k):
            prod = poly_mul_ntt(s_ntt[i], u_ntt[i])
            inner_prod_ntt = poly_add(inner_prod_ntt, prod)
        m_poly = poly_sub(v, inv_ntt(inner_prod_ntt))
        recovered_m = bytearray()
        cur_b, bit_c = 0, 0
        for val in m_poly:
            dist_0 = min(abs(val), abs(val - Q))
            dist_q2 = abs(val - Q // 2)
            bit = 1 if dist_q2 < dist_0 else 0
            cur_b |= (bit << bit_c)
            bit_c += 1
            if bit_c == 8:
                recovered_m.append(cur_b)
                cur_b, bit_c = 0, 0
            if len(recovered_m) == 32: break
        return sha3_256(bytes(recovered_m))
