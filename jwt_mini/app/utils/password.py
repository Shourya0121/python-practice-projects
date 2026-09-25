from pwdlib import PasswordHash

Password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return Password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> str:
    return Password_hash.verify(password, hashed_password)