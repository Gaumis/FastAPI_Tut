from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: str
    price: int

class ProductResponse(BaseModel):
    name: str
    description: str

    class config:
        orm_mode = True # This is used to directly serialize the SQLAlchemy object to JSON

