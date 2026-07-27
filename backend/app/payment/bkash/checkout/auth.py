import httpx

from app.core.config import settings
from app.payment.bkash.checkout.constants import *


class BkashAuth:

    def __init__(self):
        self.base_url = settings.BKASH_CHECKOUT_BASE_URL
        self.app_key = settings.BKASH_APP_KEY
        self.app_secret = settings.BKASH_APP_SECRET
        self.username = settings.BKASH_USERNAME
        self.password = settings.BKASH_PASSWORD

    async def grant_token(self) -> dict:

        url = f"{self.base_url}{GRANT_TOKEN}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": self.username,
            "password": self.password,
        }

        payload = {
            "app_key": self.app_key,
            "app_secret": self.app_secret,
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                json=payload,
                headers=headers,
            )

        print("\n========== GRANT TOKEN ==========")
        print("URL:", url)
        print("Status:", response.status_code)
        print("Headers:", response.headers)
        print("Body:")
        print(response.text)

        response.raise_for_status()

        data = response.json()

        if data.get("statusCode") != "0000":
            raise Exception(data)

        return data