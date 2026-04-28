import requests
import time

CLOUD_URL = "http://localhost:5000/upload"

def run_attack():
    print("[!] MITM ATTACK STARTING...")
    
    # The attacker tries to send a malicious payload
    fake_data = b"MALICIOUS_CMD: SHUTDOWN_HEATER"
    fake_signature = "a" * 512 # Just 512 characters of junk
    
    headers = {
        'Content-Type': 'application/octet-stream',
        'X-Signature': fake_signature
    }

    try:
        print("[!] Attempting to upload tampered data to Cloud...")
        response = requests.post(CLOUD_URL, data=fake_data, headers=headers)
        
        if response.status_code == 401:
            print(f"[*] SUCCESS: Cloud rejected the attack! Status: {response.status_code}")
            print(f"[*] Cloud Message: {response.text}")
        else:
            print(f"[#] FAILURE: Cloud accepted fake data! Status: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_attack()