from dataclasses import dataclass, field
from typing import Any


@dataclass
class AppException(Exception):
    message: str
    code: str = "INTERNAL_ERROR"
    status_code: int = 500
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class NotFoundError(AppException):
    message: str = "Resource not found"
    code: str = "NOT_FOUND"
    status_code: int = 404


@dataclass
class UnauthorizedError(AppException):
    message: str = "Authentication required"
    code: str = "UNAUTHORIZED"
    status_code: int = 401


@dataclass
class ForbiddenError(AppException):
    message: str = "Insufficient permissions"
    code: str = "FORBIDDEN"
    status_code: int = 403


@dataclass
class ValidationError(AppException):
    message: str = "Validation failed"
    code: str = "VALIDATION_ERROR"
    status_code: int = 422


@dataclass
class ConflictError(AppException):
    message: str = "Resource already exists"
    code: str = "CONFLICT"
    status_code: int = 409


@dataclass
class RateLimitError(AppException):
    message: str = "Too many requests"
    code: str = "RATE_LIMIT_EXCEEDED"
    status_code: int = 429
