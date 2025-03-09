from fastapi import APIRouter, Depends, status
from controllers.user_controller import UserController
from db_config import get_db
from schemas import Users
from sqlalchemy.orm import Session

from models.user_model import CreateUserRequest

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get("/")
async def get_all_users(db: Session=Depends(get_db)):
    users = db.query(Users).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db: Session=Depends(get_db)):
    return await UserController.create(user=user, db=db)