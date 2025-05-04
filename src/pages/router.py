from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from src.templates import templates
from src.categories.schemas import CategoryOutSchema
from src.categories.router import get_all_categories
from src.products.schemas import ProductOutSchema
from src.products.router import get_all_products, get_product

router = APIRouter(prefix='/pages', tags=['Frontend'])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/categories", response_class=HTMLResponse)
async def show_categories(request: Request,
                     categories: list[CategoryOutSchema] = Depends(get_all_categories)):
    return templates.TemplateResponse("categories.html", context={"request": request, "categories": categories})


@router.get("/products", response_class=HTMLResponse)
async def show_products(request: Request,
                        products: list[ProductOutSchema] = Depends(get_all_products)):
    return templates.TemplateResponse("products.html", context={"request": request, "products": products})

@router.get("/products/{slug}", response_class=HTMLResponse)
async def show_product(request: Request,
                       product: ProductOutSchema = Depends(get_product)):
    return templates.TemplateResponse("product_card.html", context={"request": request, "product": product})




@router.get("/user", response_class=HTMLResponse)
async def show_user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})


@router.get("/orders", response_class=HTMLResponse)
async def show_orders(request: Request):
    return templates.TemplateResponse("orders.html", {"request": request})
