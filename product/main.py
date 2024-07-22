from fastapi import FastAPI, Depends, HTTPException, status
from schemas import Product, ProductResponse
import models
from database import engine, sessionLocal
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

models.Base.metadata.create_all(engine)

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
    new_product = models.Product(name=request.name, description=request.description, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product