from httpx import AsyncClient
from aiolimiter import AsyncLimiter



class ipWhoIsManager:
    """
    Менеджер для работы с API ipwho.is
    - информация об ip адресе
    Бесплатный, PRS = 1
    """

    limiter = AsyncLimiter(1, 1)
    client = AsyncClient(base_url="http://ipwho.is", )


    async def get_host_info(self, host: str) -> str:
        async with self.limiter:
            text = ""
            response = await self.client.get(f"/{host}?lang=ru")
            host_info = response.json()

            success = host_info.get("success", False)

            if not success:
                text += host_info.get("message")
            else:
                text += host_info.get("country")
                text += host_info.get("flag", {}).get("emoji") + "\n"
                text += host_info.get("region") + "\n"
                text += host_info.get("city") + "\n"

            return text
