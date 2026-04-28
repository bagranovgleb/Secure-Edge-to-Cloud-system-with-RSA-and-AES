# Secure Storage Edge-to-Cloud 🛡️

A security-focused IoT simulation featuring a "Chain of Trust" between an MPU (Edge) and a Cloud Server.

## 🔒 Security Features
* **Secure Boot:** SHA-256 integrity check via `bootloader.py`.
* **Confidentiality:** AES-256 GCM encryption.
* **Authenticity:** RSA-PSS Digital Signatures.
* **Anti-Replay:** UTC Timestamp validation.

## 🚀 How to Run
1. Generate Keys: `python generate_keys.py`
2. Generate Integrity: `python generate_integrity.py`
3. Launch: `docker-compose up --build`

## 🧪 Testing Defenses
* Run `python hacker_sim.py` to test Replay protection.
* Run `python mitm_attack.py` to test Signature verification.