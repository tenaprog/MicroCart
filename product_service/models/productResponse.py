from pydantic import Field
from .productBase import ProductBase


class ProductResponse(ProductBase):
    product_id: str = Field(...)
