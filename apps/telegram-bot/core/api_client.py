from __future__ import annotations

import httpx

from core.config import get_bot_settings


class FindSpamAPIClient:
    """HTTP client for the FindSpam backend API.

    Instantiate once per process inside the bot lifespan, inject via dp["api_client"].
    Never instantiate at module level — httpx.AsyncClient requires a running event loop.
    """

    def __init__(self) -> None:
        settings = get_bot_settings()
        self._client = httpx.AsyncClient(
            base_url=settings.api_base_url,
            headers={
                "Authorization": f"Bearer {settings.api_service_token}",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=2.0),
        )

    async def analyze_message(self, text: str, metadata: dict) -> dict:
        response = await self._client.post(
            "/ai/predict",
            json={"text": text, "metadata": metadata},
        )
        response.raise_for_status()
        return response.json()

    async def log_moderation_event(self, payload: dict) -> dict:
        response = await self._client.post("/moderation/events", json=payload)
        response.raise_for_status()
        return response.json()

    async def check_domain_blacklist(self, domain: str) -> bool:
        response = await self._client.get(
            "/blacklist/domains/check", params={"domain": domain}
        )
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return bool(response.json().get("is_blacklisted", False))

    async def get_group_settings(self, telegram_group_id: int) -> dict:
        response = await self._client.get(f"/telegram/groups/{telegram_group_id}/settings")
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    async def update_group_settings(self, telegram_group_id: int, payload: dict) -> dict:
        response = await self._client.put(
            f"/telegram/groups/{telegram_group_id}/settings", json=payload
        )
        response.raise_for_status()
        return response.json()

    async def get_user_profile(self, telegram_user_id: int) -> dict | None:
        response = await self._client.get(f"/telegram/users/{telegram_user_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    async def get_group_stats(self, telegram_group_id: int) -> dict:
        response = await self._client.get(f"/telegram/groups/{telegram_group_id}/stats")
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        return response.json()

    async def aclose(self) -> None:
        await self._client.aclose()
