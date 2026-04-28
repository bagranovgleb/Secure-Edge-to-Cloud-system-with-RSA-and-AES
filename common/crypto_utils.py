import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import json
import time
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

class SecureMpuStorage:
    # ... keep your existing AES GCM code ...

    @staticmethod
    def generate_rsa_keys():
        """Simulates generating a device identity."""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def sign_payload(self, private_key, data: bytes):
        """Defense B: Digital Signature to prove authenticity."""
        return private_key.sign(
            data,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

    def verify_signature(self, public_key, data: bytes, signature: bytes):
        """Defense B: Cloud verifies the data wasn't tampered with."""
        try:
            public_key.verify(
                signature,
                data,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
        
        
# ... keep your existing imports ...

class SecureMpuStorage:
    # ... keep your __init__ ...

    def encrypt_with_metadata(self, data: str):
        """Adds a timestamp and UUID to prevent replay attacks."""
        payload = {
            "ts": time.time(),
            "msg_id": str(uuid.uuid4()),
            "content": data
        }
        # Turn the dictionary into a string before encrypting
        json_data = json.dumps(payload)
        return self.encrypt_data(json_data)

    def decrypt_and_verify(self, encrypted_bundle: bytes):
        """Decrypts and checks if the message is too old (Replay Defense)."""
        decrypted_json = self.decrypt_data(encrypted_bundle)
        payload = json.loads(decrypted_json)
        
        # If the message is older than 60 seconds, reject it
        if time.time() - payload['ts'] > 60:
            raise Exception("Security Alert: Possible Replay Attack or Expired Message!")
            
        return payload['content']
    
class SecureMpuStorage:
    def __init__(self, password: str):
        """
        In a real MPU, the key might be burned into the hardware (eFused).
        Here, we derive a 256-bit key from a password and a salt.
        """
        self.salt = b'mpu_edge_salt_fixed' # In production, use a unique salt per device
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = kdf.derive(password.encode())
        self.aesgcm = AESGCM(self.key)

    def encrypt_data(self, data: str) -> bytes:
        """Encrypts string data and returns a nonce + ciphertext bundle."""
        nonce = os.urandom(12)  # GCM standard nonce length
        ciphertext = self.aesgcm.encrypt(nonce, data.encode(), None)
        # We store the nonce with the data so we can decrypt it later
        return nonce + ciphertext

    def decrypt_data(self, encrypted_bundle: bytes) -> str:
        """Splits the nonce from the ciphertext and decrypts."""
        nonce = encrypted_bundle[:12]
        ciphertext = encrypted_bundle[12:]
        decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode()

# Simple usage example:
# storage = SecureMpuStorage("my-super-secret-hardware-id")
# encrypted = storage.encrypt_data("Sensitive Edge Sensor Data")