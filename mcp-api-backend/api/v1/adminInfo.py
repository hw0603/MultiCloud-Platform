from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from service import user_service

router = APIRouter()

@router.get("/")
def get_admin_info(db: Session = Depends(get_db)):
    admin = user_service.get_admin_info(db)

    return admin

