from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from jose import JWTError, jwt

from core.config.settings import get_settings
from core.exceptions.base import UnauthorizedError

settings = get_settings()

_private_key: str | None = None
_public_key: str | None = None


def _load_private_key() -> str:
    global _private_key
    if _private_key is None:
        _private_key = Path(settings.jwt_private_key_path).read_text()
    return _private_key


def _load_public_key() -> str:
    global _public_key
    if _public_key is None:
        _public_key = Path(settings.jwt_public_key_path).read_text()
    return _public_key


def create_access_token(payload: dict[str, Any]) -> str:
    expires = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    return jwt.encode(
        {**payload, "exp": expires, "type": "access"},
        _load_private_key(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            _load_public_key(),
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise UnauthorizedError(message="Invalid or expired token") from exc
