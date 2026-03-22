from aiolimiter import AsyncLimiter
from httpx import AsyncClient, RequestError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class ipWhoIsManager:
    """
    Менеджер для работы с API ipwho.is
    - информация об ip адресе
    Бесплатный, PRS = 1
    """

    limiter = AsyncLimiter(1, 1)
    client = AsyncClient(base_url="http://ipwho.is", )


    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(4),
        retry=retry_if_exception_type(RequestError),
        retry_error_callback=lambda e: "Ошибка получения данных об ip адресе"
    )
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
                text += host_info.get("flag", {"emoji": "none"}).get("emoji") + "\n"
                text += host_info.get("region") + "\n"
                text += host_info.get("city") + "\n"

            return text
