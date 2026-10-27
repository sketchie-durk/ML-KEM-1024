
from ml_kem.kem import MLKEM1024

def simulate_handshake():
    print("[Client] Generating keys...")
    kem = MLKEM1024()
    pk, sk = kem.keygen()
    
    print("[Server] Encapsulating...")
    ct, ss_server = kem.encaps(pk)
    
    print("[Client] Decapsulating...")
    ss_client = kem.decaps(ct, sk)
    
    print(f"Shared Secret Match: {ss_server == ss_client}")

if __name__ == "__main__":
    simulate_handshake()
