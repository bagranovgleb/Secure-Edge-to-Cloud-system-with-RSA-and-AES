# Secure Storage Edge-to-Cloud 🛡️

A security-focused IoT simulation featuring a complete "Chain of Trust" between an Edge device (MPU) and a Cloud Server. The project uses four layers of defense to protect data even on untrusted networks or compromised servers.

## 🔒 Security Features
* **Secure Boot:** Verifies the code's integrity using a SHA-256 hash before execution.
* **Confidentiality:** Protects data-in-transit using AES-256 GCM encryption.
* **Authenticity:** Signs data using RSA-PSS Digital Signatures to prevent tampering.
* **Anti-Replay:** Validates UTC timestamps to reject stale or replayed messages.

---

## 🚀 How to Run

### 1. Initialize the Environment
Before starting, generate the keys and the cryptographic fingerprint:

```bash
### 1. Generate the RSA and AES keys
python generate_keys.py

### 2. Generate the Secure Boot fingerprint for edge_app.py
python generate_integrity.py


### 3. Launch the System. Run the containers using Docker:

docker-compose up --build
```

## 🧪 Testing Defenses

| Script | Functionality Tested | What it checks |
| :--- | :--- | :--- |
| `python decrypt_check.py` | **Confidentiality** | Decrypts the AES ciphertext to show readable plaintext. |
| `python mitm_attack.py` | **Integrity & Authenticity** | Simulates a Man-in-the-Middle attack by tampering with data; the cloud rejects the packet (401 Error). |
| `python hacker_sim.py` | **Anti-Replay Logic** | Sends expired (old) timestamps to verify the anti-replay protection. |


## 📁 Repository Structure
edge/: Contains the MPU application and Secure Boot utilities.

cloud/: Contains the server logic handling authentication and decryption.

common/: Stores the cryptographic keys (private keys are protected via .gitignore).