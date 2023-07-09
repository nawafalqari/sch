from cryptography.fernet import Fernet

def decrypt(message: str, key: bytes) -> str:
    cipher = Fernet(key)
    nickname, message = message.split(": ")
    decrypted_message = cipher.decrypt(message.encode("utf-8")).decode("utf-8")
    
    return f"{nickname}: {decrypted_message}"