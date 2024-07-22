from fastapi import APIRouter, Depends, status
from ..schemas import Seller, SellerResponse
from sqlalchemy.orm import Session
from ..database import get_db
from passlib.context import CryptContext
from .. import models

router = APIRouter(
    tags=["Seller"],
    prefix="/sellers"
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=SellerResponse, status_code=status.HTTP_201_CREATED)
def create_seller(request: Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(username=request.username, email=request.email, password=hashed_password)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller