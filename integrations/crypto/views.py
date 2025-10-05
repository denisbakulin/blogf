from fastapi import APIRouter
from fastapi_cache.decorator import cache

from integrations.crypto.external import CryptoResponse, get_binance_client

crypto_router = APIRouter(prefix="/ext/crypto")


@crypto_router.get("")
@cache(expire=60)
async def get_crypto(
        ticker_from: str,
        ticker_to: str
) -> CryptoResponse:

    return await get_binance_client().get_crypto_info(ticker_from, ticker_to)



