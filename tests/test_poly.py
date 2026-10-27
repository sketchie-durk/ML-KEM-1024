
import unittest
from ml_kem.poly import ntt, inv_ntt, poly_add, poly_sub, poly_mul_ntt
from ml_kem.params import N, Q

class TestPolyOps(unittest.TestCase):
    def test_ntt_inv_ntt_identity(self):
        original = [i for i in range(N)]
        recovered = inv_ntt(ntt(original))
        self.assertEqual(original, recovered)

    def test_poly_mul_ntt_correctness(self):
        a = [0] * N; a[0] = 2; a[1] = 3
        b = [0] * N; b[0] = 1; b[1] = 4
        prod = inv_ntt(poly_mul_ntt(ntt(a), ntt(b)))
        self.assertEqual(prod[0], 2); self.assertEqual(prod[1], 11); self.assertEqual(prod[2], 12)

if __name__ == "__main__":
    unittest.main()
