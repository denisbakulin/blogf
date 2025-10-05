import asyncio
from functools import wraps

from fastapi import HTTPException
from httpx import HTTPStatusError, RequestError

from integrations.exceptions import ExternalApiRequestError


class ExternalAPI:
    """Класс-родитель для создания внешних API"""

    def __init__(self, path: str, api_key: str = None):
        self.path = path
        self.api_key = api_key


def safe_request(func):
    """Декоратор для отлова дефолтных ошибок httpx"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"API error: {e}")
        except RequestError as e:
            raise HTTPException(status_code=502, detail=f"Ошибка соединения: {e}")
        except ExternalApiRequestError as e:
            raise HTTPException(status_code=400, detail=e.data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Неожиданная ошибка: {e}")
    return wrapper

async def main() -> None:

    from integrations.crypto.external import get_binance_client
    from integrations.weather.external import get_openweather_client

    crypto = get_binance_client()
    temp = get_openweather_client()

    res1 = await crypto.get_crypto_info()
    res2 = await temp.get_city_weather("zelenogorsk")

    print(res1)
    print(res2)

if __name__ == "__main__":
    asyncio.run(main())

