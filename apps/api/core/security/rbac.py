from enum import StrEnum
from typing import Sequence


class UserRole(StrEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    MODERATOR = "MODERATOR"


ROLE_PERMISSIONS: dict[UserRole, frozenset[str]] = {
    UserRole.SUPER_ADMIN: frozenset({
        "moderation:read", "moderation:write", "moderation:delete",
        "analytics:read",
        "ai:read", "ai:write", "ai:retrain",
        "users:read", "users:write", "users:delete",
        "blacklist:read", "blacklist:write", "blacklist:delete",
        "audit:read",
        "system:admin",
    }),
    UserRole.ADMIN: frozenset({
        "moderation:read", "moderation:write", "moderation:delete",
        "analytics:read",
        "ai:read",
        "users:read", "users:write",
        "blacklist:read", "blacklist:write",
        "audit:read",
    }),
    UserRole.ANALYST: frozenset({
        "moderation:read",
        "analytics:read",
        "ai:read",
        "blacklist:read",
        "audit:read",
    }),
    UserRole.MODERATOR: frozenset({
        "moderation:read", "moderation:write",
        "blacklist:read", "blacklist:write",
    }),
}


def has_permission(role: UserRole, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, frozenset())


def require_permissions(role: UserRole, permissions: Sequence[str]) -> bool:
    return all(has_permission(role, p) for p in permissions)
