from fastapi import FastAPI
from . import models
from .routers import products, seller
from .database import engine

app = FastAPI(
    title="Product API",
    description="A simple API to manage products",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Kumar Gaurav",
        "url": "http://example.com/contact",
        "email": "kumargaurav1527@gmail.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },

)

app.include_router(products.router)
app.include_router(seller.router)

models.Base.metadata.create_all(engine)


