import pytest
from src.auth import hash_password, verify_password, TokenManager, generate_salt


def test_hash_password():
    salt = generate_salt()
    password = "test_password_123"
    hashed = hash_password(password, salt)

    assert hashed is not None
    assert len(hashed) == 64
    assert hashed != password


def test_verify_password():
    salt = generate_salt()
    password = "secure_pass_456"
    hashed = hash_password(password, salt)

    assert verify_password(password, hashed, salt) is True
    assert verify_password("wrong_password", hashed, salt) is False


def test_generate_salt():
    salt1 = generate_salt()
    salt2 = generate_salt()

    assert salt1 != salt2
    assert len(salt1) > 0


def test_token_manager_generate():
    manager = TokenManager(expiration_hours=24)
    token = manager.generate_token("user_123")

    assert token is not None
    assert len(token) > 0


def test_token_manager_validate():
    manager = TokenManager(expiration_hours=24)
    token = manager.generate_token("user_456")
    user_id = manager.validate_token(token)

    assert user_id == "user_456"


def test_token_manager_revoke():
    manager = TokenManager(expiration_hours=24)
    token = manager.generate_token("user_789")
    manager.revoke_token(token)

    assert manager.validate_token(token) is None
