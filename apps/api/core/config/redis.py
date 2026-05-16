from redis.asyncio import ConnectionPool, Redis

from core.config.settings import get_settings

settings = get_settings()

_pool: ConnectionPool | None = None


def get_redis_pool() -> ConnectionPool:
    global _pool
    if _pool is None:
        _pool = ConnectionPool.from_url(
            settings.redis_url,
            decode_responses=True,
            max_connections=50,
        )
    return _pool


def get_redis_client() -> Redis:
    return Redis(connection_pool=get_redis_pool())
