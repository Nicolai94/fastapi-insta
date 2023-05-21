from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
