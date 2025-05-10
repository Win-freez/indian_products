import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.categories.router import router as category_router
from src.orders.router import router as order_router
from src.pages.router import router as pages_router
from src.products.router import router as product_router
from src.users.router import router as auth_router
from src.cart.router import router as cart_router

app = FastAPI()
app_v1 = FastAPI(
    title="API v1",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.mount('/v1', app_v1)
app.mount('/static', StaticFiles(directory='static'), name='static')

app_v1.include_router(pages_router)
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
            "v1": "/v1/docs"
        }
    }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)
