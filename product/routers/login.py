from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import Login
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Seller
from .seller import pwd_context

router = APIRouter()

@router.post("/login")
def login(request: Login, db: Session = Depends(get_db)):
    user_name = request.username
    password = request.password
    check_seller = db.query(Seller).filter(Seller.username == user_name).first()
    if not check_seller:
        return {"message": "Invalid username"}
    if not pwd_context.verify(password, check_seller.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return {"message": "Login successful"}