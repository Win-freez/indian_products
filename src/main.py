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

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(cart_router)

@app.get("/")
async def root():
    return {
        "message": "Backend API for Indian Products",
        "frontend": "/pages",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="localhost", port=8000, reload=True)
