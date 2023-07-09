from cryptography.fernet import Fernet

def encrypt(message: str, key: bytes) -> bytes:
    cipher = Fernet(key)
    message = message.encode("utf-8")

    return cipher.encrypt(message)