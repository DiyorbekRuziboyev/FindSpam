import httpx

from core.config import get_bot_settings

settings = get_bot_settings()


class FindSpamAPIClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.api_base_url,
            headers={"Authorization": f"Bearer {settings.api_service_token}"},
            timeout=10.0,
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
        response = await self._client.get(f"/blacklist/domains/check?domain={domain}")
        return response.json().get("is_blacklisted", False)

    async def aclose(self) -> None:
        await self._client.aclose()


api_client = FindSpamAPIClient()
