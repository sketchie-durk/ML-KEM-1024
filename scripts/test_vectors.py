
from ml_kem.kem import MLKEM1024
import json

def generate_vectors():
    kem = MLKEM1024()
    pk, sk = kem.keygen()
    ct, ss = kem.encaps(pk)
    # Simplified vector output
    vector = {"pk_len": len(pk[0]), "ct_len": len(ct[0])}
    print(json.dumps(vector))

if __name__ == "__main__":
    generate_vectors()
