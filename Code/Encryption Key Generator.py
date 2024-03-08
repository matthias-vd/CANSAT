import secrets
new_encryption_key = secrets.token_bytes(16)
print(new_encryption_key.hex())
