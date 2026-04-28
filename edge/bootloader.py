import hashlib
import sys
import os

def check_integrity():
    print("--- MPU Secure Boot Initializing ---")
    
    # 1. Load the 'Expected' hash
    with open("common/firmware.hash", "r") as f:
        expected_hash = f.read().strip()

    # 2. Calculate the 'Actual' hash of the current code
    with open("edge_app.py", "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()

    # 3. Compare
    if actual_hash == expected_hash:
        print("[OK] Integrity Verified. Launching Firmware...")
        return True
    else:
        print("[!!!] SECURITY ALERT: FIRMWARE TAMPERING DETECTED!")
        print(f"Expected: {expected_hash}")
        print(f"Actual:   {actual_hash}")
        return False

if __name__ == "__main__":
    if check_integrity():
        # This actually launches the edge_app
        os.system("python edge_app.py")
    else:
        print("[FATAL] System Halted to prevent data leak.")
        sys.exit(1)