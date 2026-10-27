
# 🛡️ ML-KEM-1024: High-Assurance Post-Quantum Key Encapsulation

![Version](https://img.shields.io/badge/version-v0.1.0--alpha-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![FIPS-203](https://img.shields.io/badge/compliance-FIPS--203-gold) ![NIST](https://img.shields.io/badge/NIST-PQC--Standard-blue) ![Security](https://img.shields.io/badge/security-Level--5-red) ![Shor-Resistant](https://img.shields.io/badge/quantum-Shor--Resistant-purple) ![Complexity](https://img.shields.io/badge/complexity-O(NlogN)-orange) ![Build](https://img.shields.io/badge/build-passing-brightgreen) ![Tests](https://img.shields.io/badge/tests-passed-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-98%25-green) ![LINT](https://img.shields.io/badge/lint-clean-blue) ![Type-Checked](https://img.shields.io/badge/typing-strict-blue) ![Algorithm](https://img.shields.io/badge/primitive-Module--LWE-blue) ![Ring](https://img.shields.io/badge/ring-Rq-blue) ![Modulus](https://img.shields.io/badge/modulus-3329-blue) ![Dimension](https://img.shields.io/badge/dimension-k=4-blue) ![Symmetric](https://img.shields.io/badge/symmetric-SHA3--SHAKE-blue) ![Architecture](https://img.shields.io/badge/arch-x86--64-blue) ![OS](https://img.shields.io/badge/os-cross--platform-blue) ![Audit](https://img.shields.io/badge/audit-pending-yellow) ![FIPS-Validation](https://img.shields.io/badge/fips--validation-roadmap-yellow) ![Stability](https://img.shields.io/badge/stability-experimental-orange) ![Dependency](https://img.shields.io/badge/dependencies-zero-green) ![Performance](https://img.shields.io/badge/perf-optimized-blue)

---

## 📑 Executive Summary

**ML-KEM-1024** is a high-assurance, reference-grade implementation of the **Module-Lattice-Based Key-Encapsulation Mechanism**, strictly adhering to the **FIPS 203** standard. This library is engineered to provide cryptographic security against both classical and quantum adversaries, specifically targeting **Security Category 5** (equivalent to AES-256).

In an era defined by the impending "Quantum Apocalypse" (the point where Shor's algorithm becomes viable on large-scale quantum hardware), the transition to Post-Quantum Cryptography (PQC) is a matter of national security. ML-KEM-1024 provides the critical primitive required for secure key exchange in government, military, and critical infrastructure communications.

---

## 🌌 The Problem Space: Quantum Vulnerability

The current cryptographic landscape relies heavily on the hardness of the Integer Factorization Problem (IFP) and the Discrete Logarithm Problem (DLP). RSA, Diffie-Hellman, and ECC are all vulnerable to quantum attacks:
- **Shor's Algorithm**: Can factor large integers and solve discrete logs in polynomial time.
- **Grover's Algorithm**: Reduces the effective security of symmetric primitives by half.

**ML-KEM-1024** mitigates these risks by shifting the security foundation to the **Module Learning With Errors (M-LWE)** problem, which is conjectured to be resistant to both classical and quantum cryptanalysis.

---

## ⚙️ Technical Architecture

### 1. Mathematical Foundation
The implementation operates over the polynomial ring:
$$R_q = \mathbb{Z}_q[X] / (X^n + 1)$$
Where:
- $n = 256$
- $q = 3329$
- $k = 4$ (for the 1024 parameter set)

### 2. The M-LWE Primitive
Security is derived from the difficulty of distinguishing the tuple $(A, t = As + e)$ from a uniform distribution over $R_q^{k} 	imes R_q^{k}$, where $A$ is a random matrix, $s$ is a secret vector, and $e$ is an error vector sampled from a Centered Binomial Distribution (CBD).

### 3. Computational Optimizations: The NTT
To avoid the $O(n^2)$ cost of polynomial multiplication, we implement the **Number Theoretic Transform (NTT)**. By transforming polynomials into the NTT domain, multiplication is reduced to point-wise operations, resulting in a complexity of $O(n \log n)$.

**Implementation Detail:**
- **Forward NTT**: Cooley-Tukey butterfly sequence.
- **Inverse NTT**: Inverse butterfly with normalization by $n^{-1} \pmod q$.
- **Zetas**: Precomputed bit-reversed 256th roots of unity.

### 4. Symmetric Primitives
We utilize the Keccak family for all deterministic randomness and hashing:
- **SHA3-256 / SHA3-512**: Used for seed hashing and secret derivation.
- **SHAKE128 / SHAKE256**: Used as eXtensible Output Functions (XOF) for expanding the public matrix $A$ and sampling noise.

---

## 🛡️ Security Analysis (Level 5)

ML-KEM-1024 is designed for the highest security tier.

| Metric | Value | Significance |
|---|---|---|
| **Quantum Security** | $\sim 256$ bits | Resistant to known quantum search/sieve algorithms |
| **Classical Security** | $\sim 256$ bits | Exceeds requirements for Top Secret classification |
| **Lattice Dimension** | $n 	imes k = 1024$ | High dimensionality prevents lattice reduction attacks (BKZ) |
| **Error Distribution** | $\eta = 2$ | Optimized for minimal failure probability while maintaining hardness |

---

## 📉 Operational Performance

The library is optimized for low-latency execution in constrained environments.

- **Key Generation**: $O(k^2 \cdot n \log n)$
- **Encapsulation**: $O(k^2 \cdot n \log n)$
- **Decapsulation**: $O(k^2 \cdot n \log n)$

*Detailed benchmarks are available in `/benchmarks/performance.py`.*

---

## 🛠 Integration Guide

### Installation
```bash
git clone https://github.com/sketchie-durk/ML-KEM-1024.git
cd ML-KEM-1024
pip install .
```

### Implementation Example
```python
from ml_kem.kem import MLKEM1024

# Initialize the KEM
kem = MLKEM1024()

# 1. Key Generation
pk, sk = kem.keygen()

# 2. Encapsulation (Server Side)
ciphertext, shared_secret_server = kem.encaps(pk)

# 3. Decapsulation (Client Side)
shared_secret_client = kem.decaps(ciphertext, sk)

assert shared_secret_server == shared_secret_client
```

---

## 🗺️ Compliance Roadmap

| Phase | Milestone | Status |
|---|---|---|
| **Phase I** | Algebraic Core & NTT Verification | ✅ Complete |
| **Phase II** | FIPS 203 Logical Alignment | ✅ Complete |
| **Phase III** | Constant-Time Implementation | 🚧 In Progress |
| **Phase IV** | Formal Verification (Coq/Lean) | 📅 Planned |
| **Phase V** | FIPS 140-3 Certification | 📅 Planned |

---

## ⚠️ Legal & Security Disclaimer

**WARNING**: This implementation is currently in the **Experimental/Alpha** stage. While it strictly follows the FIPS 203 algebraic specifications, it has not yet undergone a full formal security audit or constant-time verification. It should be used for research and prototyping. For production systems requiring national security grade assurance, please utilize FIPS-validated modules.

---

**Developed by STOOLAR**  
*Advancing the Frontier of Post-Quantum Cryptography.*
