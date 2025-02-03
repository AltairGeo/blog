import hashlib


def create_hash(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    if not password:
        raise ValueError("Password cannot be empty")
    hashs = hashlib.md5(password.encode()).hexdigest()
    return hashs