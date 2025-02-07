from fastapi import FastAPI
from routers import products
from routers import products_images

app = FastAPI()

app.include_router(products.router)
app.include_router(products_images.router)
