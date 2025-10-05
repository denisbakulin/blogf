from httpx import AsyncClient
from pydantic import BaseModel, ValidationError

from integrations.exceptions import ExternalApiRequestError
from integrations.external_api import ExternalAPI, safe_request


class CryptoResponse(BaseModel):
    symbol: str
    price: float


class BinanceAPI(ExternalAPI):

    @safe_request
    async def get_crypto_info(
            self,
            ticker_from: str = "btc",
            ticker_to: str = "usdt"
    ) -> CryptoResponse:

        ticker_from, ticker_to = map(str.upper, (ticker_from, ticker_to))

        async with AsyncClient(base_url=self.path) as client:

            response = await client.get(
                "/api/v3/ticker/price",
                params={"symbol": f"{ticker_from}{ticker_to}"}
            )
            data = response.json()

            try:
                data = CryptoResponse.model_validate(data)

            except ValidationError:
                raise ExternalApiRequestError(data)

            return data


from functools import lru_cache


@lru_cache
def get_binance_client() -> BinanceAPI:
    return BinanceAPI("https://api.binance.com")