import httpx

from app.core.config import settings
from app.payment.bkash.tokenized.auth import BkashAuth


class BkashClient:

    def __init__(self):
        self.base_url = settings.BKASH_TOKENIZED_BASE_URL
        self.auth = BkashAuth()

    async def _headers(self) -> dict:
        token = await self.auth.grant_token()

        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": token["id_token"],
            "X-App-Key": settings.BKASH_APP_KEY,
        }

    async def post(
        self,
        endpoint: str,
        payload: dict,
    ) -> dict:

        headers = await self._headers()

        async with httpx.AsyncClient(timeout=30) as client:
            print("POST URL:", f"{self.base_url}{endpoint}")
            print("HEADERS:", headers)
            print("PAYLOAD:", payload)
            
            response = await client.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                headers=headers,
            )
            print("STATUS:", response.status_code)
            print("BODY:", response.text)

        return response.json()

    async def get(
        self,
        endpoint: str,
        params: dict,
    ) -> dict:

        headers = await self._headers()

        async with httpx.AsyncClient(timeout=30) as client:

            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers=headers,
            )

        return response.json()