import os
import time
import json
from flask import Flask, request, abort
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from common.crypto_utils import SecureMpuStorage

app = Flask(__name__)
DB_PATH = "./database"
HARDWARE_SECRET = "mpu-device-serial-998877" # Cloud needs this to check Defense
secure_storage = SecureMpuStorage(HARDWARE_SECRET)

if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

def get_edge_public_key():
    with open("common/edge_public_key.pem", "rb") as key_file:
        return serialization.load_pem_public_key(key_file.read())

@app.route('/upload', methods=['POST'])
def upload_data():
    signature_hex = request.headers.get('X-Signature')
    encrypted_blob = request.data

    if not signature_hex:
        abort(401, "Unsigned request")

    # 1. VERIFY SIGNATURE (Defense B)
    try:
        public_key = get_edge_public_key()
        public_key.verify(
            bytes.fromhex(signature_hex),
            encrypted_blob,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
    except Exception:
        print("[!!!] TAMPERING DETECTED")
        abort(401, "Invalid Signature")

    # 2. VERIFY FRESHNESS (Defense E: Anti-Replay)
    try:
        decrypted_json = secure_storage.decrypt_data(encrypted_blob)
        data = json.loads(decrypted_json)
        
        # Check if message is older than 60 seconds
        if time.time() - data['ts'] > 60:
            print("[!!!] REPLAY ATTACK DETECTED: Message expired")
            abort(401, "Message Expired - Possible Replay")
            
        print(f"[+] Verified Fresh: {data['payload']}")
    except Exception as e:
        print(f"[!] Decryption failed during verification: {e}")
        abort(400, "Malformed Secure Envelope")

    # 3. STORE
    filename = f"verified_{int(time.time())}.bin"
    with open(os.path.join(DB_PATH, filename), "wb") as f:
        f.write(encrypted_blob)
        
    return {"status": "success"}, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)