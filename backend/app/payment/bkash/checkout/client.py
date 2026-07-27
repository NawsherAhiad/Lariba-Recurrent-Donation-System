import httpx

from app.core.config import settings
from app.payment.bkash.checkout.auth import BkashAuth


class BkashClient:

    def __init__(self):
        self.base_url = settings.BKASH_CHECKOUT_BASE_URL
        self.auth = BkashAuth()

    async def _headers(self) -> dict:
        token = await self.auth.grant_token()

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token["id_token"],
            "X-APP-Key": settings.BKASH_APP_KEY,
        }

    async def post(
        self,
        endpoint: str,
        payload: dict,
    ) -> dict:

        headers = await self._headers()

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                headers=headers,
            )

        print("\n========== CHECKOUT POST ==========")
        print("URL:", f"{self.base_url}{endpoint}")
        print("Headers:", headers)
        print("Payload:", payload)
        print("Status:", response.status_code)
        print("Body:", response.text)

        response.raise_for_status()

        return response.json()