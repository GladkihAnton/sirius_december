import hashlib

# хеширование пароля
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()
