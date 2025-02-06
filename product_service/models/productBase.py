from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal


class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    sizes: List[str] = Field(
        ["one size"],
        description="List of product sizes, default is ['one size']"
    )
    image: str = Field(..., description="Link to image on S3 bucket")
