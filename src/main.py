from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware

from src.cart.router import router as cart_router
from src.categories.router import router as category_router
from src.middleware.cash_lifetime_middleware import CashLifetimeMiddleware
from src.orders.router import router as order_router
from src.pages.router import router as pages_router
from src.products.router import router as product_router
from src.users.router import router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app_v1 = FastAPI(
    title="API v1",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app_pages = FastAPI(
    title="Frontend",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost",
    "https://example.com",
    "null"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   )
app.add_middleware(CashLifetimeMiddleware, divide_number=3)

app.mount('/v1', app_v1)
app.mount('/pages', app_pages)
app.mount('/static', StaticFiles(directory='static'), name='static')

app_pages.include_router(pages_router)
app_v1.include_router(auth_router)
app_v1.include_router(category_router)
app_v1.include_router(product_router)
app_v1.include_router(order_router)
app_v1.include_router(cart_router)


@app.get("/")
def main_root():
    return {
        "message": "Main API entry",
        "versions": {
            "v1": "/v1/docs",
            "frontend": "/pages/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)
