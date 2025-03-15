from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib

# Generate AES-256 key
def generate_key():
    return hashlib.sha256("your_secret_key".encode()).digest()

# Encrypt data using AES-256
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Decrypt data using AES-256
def decrypt_data(iv, ct, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode()

if __name__ == '__main__':
    key = generate_key()
    iv, ct = encrypt_data("Sensitive Data Example", key)
    print(f"Encrypted: IV={iv} CT={ct}")
    decrypted_data = decrypt_data(iv, ct, key)
    print(f"Decrypted: {decrypted_data}")
