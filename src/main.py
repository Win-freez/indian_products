import uvicorn
from fastapi import FastAPI

from src.categories.router import router as category_router
from src.orders.router import router as order_router
from src.products.router import router as product_router
from src.users.router import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(order_router)



@app.get('/')
async def welcome():
    return {'message': 'start page'}


if __name__ == "__main__":
    uvicorn.run('src.main:app', host='localhost', port=8000, reload=True)
