
# FIPS 203 Mapping

| FIPS 203 Section | Implementation File | Function |
|---|---|---|
| Algorithm 1 (ML-KEM.KeyGen) | ml_kem/kem.py | MLKEM1024.keygen |
| Algorithm 2 (ML-KEM.Encaps) | ml_kem/kem.py | MLKEM1024.encaps |
| Algorithm 3 (ML-KEM.Decaps) | ml_kem/kem.py | MLKEM1024.decaps |
| Algorithm 4 (NTT) | ml_kem/poly.py | ntt |
| Algorithm 5 (invNTT) | ml_kem/poly.py | inv_ntt |
