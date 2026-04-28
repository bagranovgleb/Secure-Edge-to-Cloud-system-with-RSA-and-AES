import requests

# This script simulates an attacker trying to intercept the Edge's message
# and change the 'Temperature' data to something dangerous.

EDGE_PAYLOAD = b"..." # Imagine the attacker caught this on the wire

def simulate_mitm_attack():
    print("[!] Intercepting Edge communication...")
    # Attacker tries to change the data (Tampering)
    malicious_payload = EDGE_PAYLOAD + b"modified_by_attacker"
    
    print("[!] Sending tampered data to Cloud...")
    response = requests.post("http://localhost:5000/upload", data=malicious_payload)
    print(f"Cloud Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    simulate_mitm_attack()