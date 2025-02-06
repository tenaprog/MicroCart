from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List

from models.productCreate import ProductCreate
from models.productResponse import ProductResponse
from models.productUpdate import ProductUpdate

from utils.db import create_product, get_product_by_id, get_all_products, update_product, delete_product
from utils.auth import verify_token_from_user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/products", response_model=ProductResponse)
def create_product_route(product: ProductCreate, token: str = Depends(oauth2_scheme)):
    verify_token_from_user_service(token, True)
    product_data = product.model_dump()
    created_product = create_product(product_data)
    return ProductResponse(**created_product)


@router.get("/products", response_model=List[ProductResponse])
def get_all_products_route():
    # no authentication needed
    products = get_all_products()
    return [ProductResponse(**product) for product in products]


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product_route(product_id: str, token: str = Depends(oauth2_scheme)):
    verify_token_from_user_service(token, False)
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product)


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product_route(product_id: str, product: ProductUpdate, token: str = Depends(oauth2_scheme)):
    verify_token_from_user_service(token, True)
    update_expression = []
    expression_attribute_values = {}

    for key, value in product.dict(exclude_unset=True).items():
        update_expression.append(f"{key} = :{key}")
        expression_attribute_values[f":{key}"] = value

    if not update_expression:
        raise HTTPException(
            status_code=400, detail="No data provided for update")

    update_expression = f"SET {', '.join(update_expression)}"
    update_product(product_id, update_expression, expression_attribute_values)

    updated_product = get_product_by_id(product_id)
    return ProductResponse(**updated_product)


@router.delete("/products/{product_id}", status_code=204)
def delete_product_route(product_id: str, token: str = Depends(oauth2_scheme)):
    verify_token_from_user_service(token, True)
    delete_product(product_id)
    return {}
