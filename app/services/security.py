from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    """
    Хеширование пароля.

    Args:
        password (str): Нехешированный пароль.

    Returns:
        str: Хешированный пароль.
    """
    hashed_password = bcrypt.hash(password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка пароля.

    Args:
        plain_password (str): Нехешированный пароль для проверки.
        hashed_password (str): Хешированный пароль.

    Returns:
        bool: True, если пароль совпадает, в противном случае False.
    """
    return bcrypt.verify(plain_password, hashed_password)
