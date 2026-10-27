
from ml_kem.kem import MLKEM1024
import time

def benchmark_keygen(count=10):
    kem = MLKEM1024()
    start = time.time()
    for _ in range(count):
        kem.keygen()
    print(f"Generated {count} keys in {time.time() - start:.4f}s")

if __name__ == "__main__":
    benchmark_keygen()
