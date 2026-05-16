import time

import structlog
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from core.config.settings import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

_LOGIN_PATHS = {"/api/v1/auth/login"}
_LOGIN_LIMIT = settings.rate_limit_login_per_15min
_LOGIN_WINDOW = 15 * 60  # 15 minutes in seconds
_API_LIMIT = settings.rate_limit_api_per_minute
_API_WINDOW = 60  # 1 minute in seconds


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: object, redis: Redis) -> None:  # type: ignore[override]
        super().__init__(app)
        self._redis = redis

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        ip = _client_ip(request)
        path = request.url.path

        is_login = path in _LOGIN_PATHS
        limit = _LOGIN_LIMIT if is_login else _API_LIMIT
        window = _LOGIN_WINDOW if is_login else _API_WINDOW
        bucket = "login" if is_login else "api"

        try:
            key = f"rate_limit:{bucket}:{ip}"
            now = int(time.time())
            window_start = now - window

            pipe = self._redis.pipeline()
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zadd(key, {str(now): now})
            pipe.zcard(key)
            pipe.expire(key, window)
            results = await pipe.execute()

            count: int = results[2]
            if count > limit:
                retry_after = window
                logger.warning(
                    "rate_limit_exceeded",
                    ip=ip,
                    path=path,
                    count=count,
                    limit=limit,
                )
                return ORJSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests. Please slow down.",
                        }
                    },
                    headers={"Retry-After": str(retry_after)},
                )
        except Exception:
            # Fail open — Redis unavailability must not block requests
            logger.warning("rate_limit_redis_unavailable", ip=ip, path=path)

        return await call_next(request)
