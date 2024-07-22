from fastapi import FastAPI, Depends, HTTPException, status
from schemas import Product, ProductResponse, Seller, SellerResponse
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

app = FastAPI()

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/products/{id}")
def update_product(id: int, request: Product, db: Session = Depends(get_db)):
    try:
        product = db.query(models.Product).filter(models.Product.id == id)
        if not product.first():
            raise HTTPException(status_code=404, detail="Product not found")
        product.update(request.dict())
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Product updated successfully"}

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product



@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=request.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.post("/sellers", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
def create_seller(request: Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller