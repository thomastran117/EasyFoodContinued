import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest
from jose import jwt as jose_jwt
from unittest.mock import patch
from service.tokenService import TokenService
from utilities.errorRaiser import UnauthorizedException


# ---------------------------------------------------------------------------
# Mock Cache Service
# ---------------------------------------------------------------------------
class MockCacheService:
    """Simple in-memory cache mock that mimics CacheService API."""

    def __init__(self):
        self.store = {}

    def set(self, key, value, expire=None, as_json=True):
        self.store[key] = value
        return True

    def get(self, key, as_json=True):
        return self.store.get(key)

    def delete(self, key):
        return bool(self.store.pop(key, None))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def mock_cache():
    return MockCacheService()


@pytest.fixture
def token_service(mock_cache):
    """Provide TokenService with mocked env settings."""
    with patch("config.environmentConfig.settings", autospec=True) as mock_settings:
        mock_settings.algorithm = "HS256"
        mock_settings.jwt_secret_access = "access_secret"
        mock_settings.jwt_secret_refresh = "refresh_secret"
        mock_settings.jwt_secret_verify = "verify_secret"
        yield TokenService(mock_cache)


# ---------------------------------------------------------------------------
# Token creation and decoding
# ---------------------------------------------------------------------------
def test_create_access_token_and_decode(token_service):
    """Ensure access token encodes and decodes correctly."""
    payload = {"id": "123", "email": "test@example.com", "role": "user"}
    token = token_service.create_access_token(payload)

    # Decode using the exact same secret from the service itself
    decoded = jose_jwt.decode(
        token,
        token_service.JWT_SECRET_ACCESS,
        algorithms=[token_service.algorithm],
        options={"verify_exp": False},
    )
    assert decoded["email"] == "test@example.com"
    assert decoded["id"] == "123"
    assert "exp" in decoded


def test_create_refresh_token_stores_in_cache(token_service, mock_cache):
    data = {"id": "123", "email": "test@example.com", "role": "user"}
    token = token_service.create_refresh_token(data, remember=False)
    key = f"refresh:{token}"
    assert key in mock_cache.store


def test_create_verification_token_stores_in_cache(token_service, mock_cache):
    token = token_service.create_verification_token("user@example.com", "pw123")
    key = f"verify:{token}"
    assert key in mock_cache.store


def test_verify_refresh_token_valid(token_service):
    """Valid refresh token should return its payload."""
    data = {"id": "1", "email": "a@b.com", "role": "user", "remember": False}
    token = token_service.create_refresh_token(data, remember=False)
    payload = token_service.verify_refresh_token(token)
    assert payload["email"] == "a@b.com"


def test_verify_refresh_token_invalid_signature(token_service):
    """Invalid secret should raise UnauthorizedException."""
    fake_token = jose_jwt.encode({"id": "x"}, "wrong_secret", algorithm="HS256")
    with pytest.raises(UnauthorizedException):
        token_service.verify_refresh_token(fake_token)


def test_verify_refresh_token_expired_or_revoked(token_service, mock_cache):
    """If token missing in cache, must raise UnauthorizedException."""
    data = {"id": "x", "email": "t@t.com", "role": "u", "remember": False}
    token = token_service.create_refresh_token(data, remember=False)
    mock_cache.delete(f"refresh:{token}")  # simulate revoked
    with pytest.raises(UnauthorizedException):
        token_service.verify_refresh_token(token)


# ---------------------------------------------------------------------------
# Combined token flows
# ---------------------------------------------------------------------------
def test_generate_tokens_returns_valid_pair(token_service):
    """Access + refresh tokens both decode correctly."""
    access, refresh = token_service.generate_tokens("1", "e@e.com", "admin", True)

    decoded_access = jose_jwt.decode(
        access,
        token_service.JWT_SECRET_ACCESS,
        algorithms=[token_service.algorithm],
        options={"verify_exp": False},
    )
    decoded_refresh = jose_jwt.decode(
        refresh,
        token_service.JWT_SECRET_REFRESH,
        algorithms=[token_service.algorithm],
        options={"verify_exp": False},
    )

    assert decoded_access["email"] == "e@e.com"
    assert decoded_refresh["role"] == "admin"


def test_rotate_refresh_token_creates_new_pair(token_service):
    data = {"id": "1", "email": "x@y.com", "role": "user", "remember": False}
    old = token_service.create_refresh_token(data, remember=False)
    access, new_refresh, email = token_service.rotate_refresh_token(old)
    assert email == "x@y.com"
    assert old != new_refresh
    assert isinstance(access, str)


def test_invalidate_refresh_token(token_service, mock_cache):
    """Ensure invalidation deletes refresh token from cache."""
    data = {"id": "1", "email": "x@y.com", "role": "user", "remember": False}
    token = token_service.create_refresh_token(data, remember=False)
    token_service.invalidate_refresh_token(token)
    assert f"refresh:{token}" not in mock_cache.store
