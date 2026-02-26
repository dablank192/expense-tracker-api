import uuid
from pwdlib import PasswordHash


#USERNAME GENERATOR
def generate_random_username() -> str:
    random_suffix = uuid.uuid4().hex[:8]
    return f"user_{random_suffix}"


#PASSWORD HASHER
password_hash = PasswordHash.recommended()

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)