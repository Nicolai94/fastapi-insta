from fastapi import APIRouter, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.schemas.product import ProductBase

templates_router = APIRouter(prefix="/templates", tags=["templates"])

templates = Jinja2Templates(directory="templates")


@templates_router.get("/products/{id}", response_class=HTMLResponse)
def get_product(id: int, product: ProductBase, request: Request):
    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "id": id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
        },
    )
