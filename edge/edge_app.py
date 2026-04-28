import time
import os
import requests
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from common.crypto_utils import SecureMpuStorage

# --- Configuration ---
HARDWARE_SECRET = "mpu-device-serial-998877"
CLOUD_URL = os.getenv("CLOUD_URL", "http://cloud-app:5000/upload")
PRIVATE_KEY_PATH = "common/edge_private_key.pem"

secure_storage = SecureMpuStorage(HARDWARE_SECRET)

def get_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        return serialization.load_pem_private_key(key_file.read(), password=None)

def simulate_sensor_reading():
    return {"temp": 24.5, "status": "OK", "unit": "Celsius"}

def main():
    print("--- Edge MPU Simulator (Enhanced Security) ---")
    
    while True:
        try:
            # 1. CAPTURE & ENVELOPE (Defense E: Anti-Replay)
            sensor_data = simulate_sensor_reading()
            envelope = {
                "ts": time.time(),           # Freshness component
                "payload": sensor_data
            }
            json_payload = json.dumps(envelope)

            # 2. ENCRYPT (Defense C: Cloud Breach)
            encrypted_blob = secure_storage.encrypt_data(json_payload)
            
            # 3. SIGN (Defense B: Anti-Tampering)
            priv_key = get_private_key()
            signature = priv_key.sign(
                encrypted_blob,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )

            # 4. SEND
            headers = {'X-Signature': signature.hex()}
            response = requests.post(CLOUD_URL, data=encrypted_blob, headers=headers, timeout=5)

            print(f"[{time.strftime('%H:%M:%S')}] Sent: {json_payload}")
            print(f"Cloud Response: {response.status_code}")

        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()