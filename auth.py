import hashlib

def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

def is_admin(password: str) -> bool:
    return password == "admin123"
