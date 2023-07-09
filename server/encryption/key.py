from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()