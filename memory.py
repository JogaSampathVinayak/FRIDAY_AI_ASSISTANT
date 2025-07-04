import json
from cryptography.fernet import Fernet

KEY_FILE = "memory/secret.key"
MEMORY_FILE = "memory/secure_memory.json"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return Fernet(key)

def save_memory(key, data):
    f = load_key()
    encrypted = f.encrypt(json.dumps(data).encode())
    with open(MEMORY_FILE, "wb") as f:
        f.write(encrypted)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    f = load_key()
    with open(MEMORY_FILE, "rb") as file:
        decrypted = f.decrypt(file.read())
    return json.loads(decrypted)
