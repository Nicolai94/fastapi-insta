import time
from typing import Optional, List

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    Response,
    Header,
    Cookie,
    Form,
)
from fastapi.responses import HTMLResponse, PlainTextResponse

from src.models.products import products
from log import log

products_router = APIRouter(prefix="/product", tags=["product"])


async def time_consuming_functionality():
    time.sleep(5)
    return "ok"


@products_router.post("/new")
def create_product(name: str = Form(...)):
    products.append(name)
    return products


@products_router.get("/all")
async def get_all_products():
    await time_consuming_functionality()
    log("MyApi", "Call to get all products")
    data = " ".join(products)
    response = Response(content=data, media_type="text/plain")
    response.set_cookie(key="test_cookie", value="test_cookie_value")
    return response


# здесь применение новых headers
@products_router.get("/withheader")
def get_products(
    response: Response,
    custom_header: Optional[List[str]] = Header(None),
    test_cookie: Optional[str] = Cookie(None),
):
    if custom_header:
        response.headers["custom_response_header"] = " and".join(custom_header)
    return {"data": products, "custom_header": custom_header, "my_cookie": test_cookie}


@products_router.get(
    "/{id}",
    responses={
        200: {
            "content": {"text/html": {"example": "<div>Product</div>"}},
            "description": "Return the HTML for an object",
        },
        404: {
            "content": {"text/plain": {"example": "<div>Product not found</div>"}},
            "description": "A clear text error message",
        },
    },
)
def get_product(id: int):
    if id > len(products):
        out = "Product not available"
        return PlainTextResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=out, media_type="text/plain"
        )
    else:
        product = products[id]
        out = f"""
        <head>
            <style>
            .product {{
                width: 500px;
                height:30px;
                border: 2px inset green;
                background-color: lightblue;
                text-align: center;
                }}
            </style>
        </head>
        <div class="product">{product}</div>        
        """
        return HTMLResponse(content=out, media_type="text/html")
