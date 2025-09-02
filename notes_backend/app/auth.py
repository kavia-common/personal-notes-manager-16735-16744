import hmac
import hashlib
from typing import Optional
from flask import request


def _pbkdf2_sha256(password: str, salt: str) -> str:
    """Simple salted password hashing using sha256."""
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 310000)
    return h.hex()


# PUBLIC_INTERFACE
def hash_password(password: str, salt: str) -> str:
    """Hash password with a salt."""
    return _pbkdf2_sha256(password, salt)


# PUBLIC_INTERFACE
def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    """Verify password against expected hash."""
    return hmac.compare_digest(hash_password(password, salt), expected_hash)


# PUBLIC_INTERFACE
def get_bearer_token() -> Optional[str]:
    """Extract a Bearer token from the Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None
