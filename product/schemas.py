from pydantic import BaseModel

class Seller(BaseModel):
    username: str
    email: str
    password: str

class SellerResponse(BaseModel):
    username: str
    email: str

    class config:
        orm_mode = True

class Product(BaseModel):
    name: str
    description: str
    price: int
    seller_id: int

class ProductResponse(BaseModel):
    name: str
    description: str
    seller : SellerResponse

    class config:
        orm_mode = True # This is used to directly serialize the SQLAlchemy object to JSON

class Login(BaseModel):
    username: str
    password: str

