import hashlib
import secrets
import time
from typing import Optional, Dict


class TokenManager:
    def __init__(self, expiration_hours: int = 24):
        self.expiration_hours = expiration_hours
        self.revoked_tokens: set = set()
        self.token_store: Dict[str, dict] = {}

    def generate_token(self, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        self.token_store[token] = {
            "user_id": user_id,
            "created_at": time.time(),
            "expires_at": time.time() + (self.expiration_hours * 3600),
        }
        return token

    def validate_token(self, token: str) -> Optional[str]:
        if token in self.revoked_tokens:
            return None

        if token not in self.token_store:
            return None

        token_data = self.token_store[token]
        if time.time() > token_data["expires_at"]:
            return None

        return token_data["user_id"]

    def revoke_token(self, token: str) -> bool:
        self.revoked_tokens.add(token)
        if token in self.token_store:
            del self.token_store[token]
        return True


def hash_password(password: str, salt: str) -> str:
    combined = password + salt
    return hashlib.sha256(combined.encode()).hexdigest()


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    computed_hash = hash_password(password, salt)
    return computed_hash == stored_hash


def generate_salt() -> str:
    return secrets.token_hex(16)


def login(username: str, password: str, token_manager: TokenManager) -> Optional[str]:
    """
    Authenticate user and generate session token.

    Args:
        username: User's username
        password: User's password
        token_manager: TokenManager instance for token generation

    Returns:
        Session token if authentication successful, None otherwise
    """
    # TODO: Integrate with actual user database
    # For now, this is a placeholder implementation
    user_id = f"user_{username}"
    token = token_manager.generate_token(user_id)
    return token


def logout(token: str, token_manager: TokenManager) -> bool:
    """
    Logout user by revoking their session token.

    Args:
        token: Session token to revoke
        token_manager: TokenManager instance for token revocation

    Returns:
        True if logout successful, False otherwise
    """
    return token_manager.revoke_token(token)
