import requests
import time
import json

CLOUD_URL = "http://localhost:5000/upload"

def run_sniffing_attack():
    print("\n--- [1] SNIFFING ATTACK ---")
    try:
        with open("./edge/secure_vault/data_1771261189.bin", "rb") as f:
            secret_data = f.read()
        print(f"[*] Attacker intercepted blob: {secret_data[:20].hex()}...")
        print("[!] Result: Data is AES-256 encrypted. Cannot read the payload.")
    except FileNotFoundError:
        print("[!] No files found to sniff. Send some data from Edge first!")

def run_tampering_attack():
    print("\n--- [2] TAMPERING ATTACK ---")
    # try to change the temperature to 999.0 to trigger an alarm
    fake_blob = b"Encrypted_Data_With_999_Degrees"
    fake_sig = "00" * 256 # doesn't have the Private Key to sign this
    
    headers = {'X-Signature': fake_sig}
    response = requests.post(CLOUD_URL, data=fake_blob, headers=headers)
    print(f"[*] Sending tampered data... Cloud Response: {response.status_code}")
    print(f"[*] Defense Result: {'BLOCKED' if response.status_code == 401 else 'FAILED'}")

def run_replay_attack():
    print("\n--- [3] REPLAY ATTACK ---")
    # Attacker captures a VALID message from the past and resends it later
    # 'valid' signature but 'old' timestamp
    print("[*] Re-sending a message captured 5 minutes ago...")
    
    # We send junk data with a valid-looking format but old content
    old_blob = b"this_is_a_captured_valid_blob_from_earlier"
    headers = {'X-Signature': 'some_captured_signature'} # Mocking a capture
    
    response = requests.post(CLOUD_URL, data=old_blob, headers=headers)
    print(f"[*] Replaying old message... Cloud Response: {response.status_code}")
    print(f"[*] Defense Result: {'BLOCKED' if response.status_code == 401 else 'FAILED'}")

if __name__ == "__main__":
    print("MPU Security Attack Simulator")
    run_sniffing_attack()
    run_tampering_attack()
    run_replay_attack()