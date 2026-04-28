import hashlib

def generate_fingerprint():
    with open("edge/edge_app.py", "rb") as f:
        code = f.read()
        fingerprint = hashlib.sha256(code).hexdigest()
    
    with open("common/firmware.hash", "w") as f:
        f.write(fingerprint)
    print(f"[+] Firmware Fingerprint Created: {fingerprint}")

if __name__ == "__main__":
    generate_fingerprint()