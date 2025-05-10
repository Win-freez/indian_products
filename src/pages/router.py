from typing import Annotated

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.categories.router import get_all_categories
from src.categories.schemas import CategoryOutSchema
from src.products.router import get_all_products, get_product, products_by_category
from src.products.schemas import ProductOutSchema
from src.templates import templates
from src.users.schemas import UserOutSchema
from src.users.router import get_user_info, get_user_using_token
from src.users.dependencies import get_access_token
from src.users.models import User
from src.database import get_db
from src.orders.schemas import OrderOutSchema
from src.orders.router import get_order, get_orders

router = APIRouter(prefix='/pages', tags=['Frontend'])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    return templates.TemplateResponse('index.html',
                                      context={"request": request})


@router.get('/categories', response_class=HTMLResponse)
async def show_categories(request: Request,
                          categories: list[CategoryOutSchema] = Depends(get_all_categories)):
    return templates.TemplateResponse("categories.html",
                                      context={"request": request, "categories": categories})


@router.get("/products", response_class=HTMLResponse)
async def show_products(request: Request,
                        products: list[ProductOutSchema] = Depends(get_all_products)):
    return templates.TemplateResponse("products.html",
                                      context={"request": request, "products": products})


@router.get("/products/{slug}", response_class=HTMLResponse)
async def show_product(request: Request,
                       product: ProductOutSchema = Depends(get_product)):
    return templates.TemplateResponse("product_card.html",
                                      context={"request": request, "product": product})


@router.get("/categories/{slug}", response_class=HTMLResponse)
async def show_filter_products(request: Request, products: list[ProductOutSchema] = Depends(products_by_category)):
    return templates.TemplateResponse("products.html",
                                      context={"request": request, "products": products})



@router.get("/registration", response_class=HTMLResponse)
async def show_registration(request: Request):
    return templates.TemplateResponse("registration.html",
                                      context={"request": request})


@router.get('/login', response_class=HTMLResponse)
async def show_login(request: Request):
    return templates.TemplateResponse("login.html",
                                      context={"request": request})


@router.get('/profile', response_class=HTMLResponse)
async def show_profile(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    try:
        user = get_user_using_token(db=db, token=get_access_token(request))
        return templates.TemplateResponse("profile.html", context={"request": request, "user": user})
    except HTTPException as e:
        if e.status_code == status.HTTP_401_UNAUTHORIZED:
            return templates.TemplateResponse("login.html", context={"request": request})
        else:
            raise e


@router.get('/orders', response_class=HTMLResponse)
async def show_orders(request: Request, orders: list[OrderOutSchema] = Depends(get_orders)):
    return templates.TemplateResponse("orders.html", request=request, context={"request": request, "orders": orders})

@router.get('/orders/{object_id}', response_class=HTMLResponse)
async def show_order(request: Request, order: OrderOutSchema = Depends(get_order)):
    return templates.TemplateResponse("order.html", request=request, context={"request": request,
                                                                               "order": order})

