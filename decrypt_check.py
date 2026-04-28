from common.crypto_utils import SecureMpuStorage
import os

# This MUST match the HARDWARE_SECRET used in edge_app.py
HARDWARE_SECRET = "mpu-device-serial-998877"
secure_storage = SecureMpuStorage(HARDWARE_SECRET)

def decrypt_file(file_path):
    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Use our utility to decrypt
        decrypted_text = secure_storage.decrypt_data(encrypted_data)
        print(f"--- Decrypted Content of {os.path.basename(file_path)} ---")
        print(decrypted_text)
        print("-" * 50)
    except Exception as e:
        print(f"Error decrypting {file_path}: {e}")

# Change this to match a filename you see in your cloud/database folder
file_to_read = "./cloud/database/verified_1771323131.bin" 

if __name__ == "__main__":
    if os.path.exists(file_to_read):
        decrypt_file(file_to_read)
    else:
        print(f"File {file_to_read} not found. Please check the filename in your folder.")