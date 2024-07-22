from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import Product, ProductResponse
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import models

router = APIRouter(
    tags=["Products"],
    prefix="/products"
)

@router.put("/{id}", summary="Update a product", description="Update a existing product")
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

@router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get("/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(request: Product, db: Session = Depends(get_db)):
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=request.seller_id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product