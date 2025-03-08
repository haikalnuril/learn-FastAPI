from fastapi import APIRouter, Depends
from db_config import get_db
from models import Users
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get("/")
async def get_all_users(db: Session=Depends(get_db)):
    users = db.query(Users).all()
    return users