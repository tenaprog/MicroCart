from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductUpdate(BaseModel):
    product_name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    sizes: Optional[List[str]] = Field(
        None, description="List of product sizes")
    image: Optional[str] = Field(
        None, description="Link to image on S3 bucket")
