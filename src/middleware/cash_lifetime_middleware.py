import re
from typing import Callable, Awaitable

from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware


class CashLifetimeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, divide_number: int):
        super().__init__(app)
        self.divide_number = divide_number

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response: Response = await call_next(request)

        cache_control = response.headers.get('Cache-Control')
        if cache_control and 'max-age' in cache_control:
            new_cache_control = self._reduce_max_age(cache_control, self.divide_number)

            response.headers['Cache-Control'] = new_cache_control
        return response

    @staticmethod
    def _reduce_max_age(cache_control_header: str, divide_number: int) -> str:
        def replacer(match):
            try:
                value = int(match.group(1))
                return f"max-age={value // divide_number}"
            except (ValueError, TypeError):
                return match.group(0)

        return re.sub(r"max-age=(\d+)", replacer, cache_control_header)
