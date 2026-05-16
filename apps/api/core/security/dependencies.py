from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.db.enums import UserRole
from core.exceptions.base import ForbiddenError, UnauthorizedError
from core.security.jwt import decode_access_token
from core.security.rbac import require_permissions

_bearer = HTTPBearer(auto_error=False)


@dataclass(frozen=True)
class AuthenticatedUser:
    id: UUID
    email: str
    role: UserRole


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> AuthenticatedUser:
    if credentials is None:
        raise UnauthorizedError(message="Missing authorization header")

    payload = decode_access_token(credentials.credentials)

    if payload.get("type") != "access":
        raise UnauthorizedError(message="Invalid token type")

    try:
        return AuthenticatedUser(
            id=UUID(payload["sub"]),
            email=payload["email"],
            role=UserRole(payload["role"]),
        )
    except (KeyError, ValueError) as exc:
        raise UnauthorizedError(message="Malformed token payload") from exc


def require_role(*permissions: str):
    async def _dependency(
        current_user: AuthenticatedUser = Depends(get_current_user),
    ) -> AuthenticatedUser:
        if not require_permissions(current_user.role, permissions):
            raise ForbiddenError(
                message=f"Required permissions: {', '.join(permissions)}"
            )
        return current_user

    return _dependency
