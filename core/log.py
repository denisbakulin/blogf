from loguru import logger
from pathlib import Path
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from time import monotonic_ns


path_dir = Path(__file__).parent.parent

logger.add(
    path_dir / "app_log.log",
    level="DEBUG",
    format="{time} {level} {message}",
    rotation="10 MB",
    retention="7 days",
    compression="zip"
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = monotonic_ns()
        logger.info(f"Request: {request.method} {request.url} from {request.client.host}")

        response = await call_next(request)

        process_time = (monotonic_ns() - start_time) / 10**9

        response_str = (f"Response: {request.method} {request.url} "
                        f"Status: {response.status_code} "
                        f"Time: {process_time:.4f}s")


        logger.error(response_str) \
            if response.status_code >= 400 \
            else logger.info(response_str)

        return response


