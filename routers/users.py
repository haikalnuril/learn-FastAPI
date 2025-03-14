from fastapi import APIRouter, Depends, status
from controllers.user_controller import UserController
from db_config import get_db
from schemas import Users
from sqlalchemy.orm import Session
from middlewares import auth_middleware

from models.user_model import CreateUserRequest, LoginUserRequest, UpdateUserRequest

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

@router.get("/")
async def get_all_users(db: Session=Depends(get_db)):
    users = db.query(Users).all()
    return users

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginUserRequest, db: Session = Depends(get_db)):
    return await UserController.login(request=request, db=db)

protected_router = APIRouter(dependencies=[Depends(auth_middleware)])

@protected_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db: Session=Depends(get_db)):
    return await UserController.create(user=user, db=db)

@protected_router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UpdateUserRequest, db: Session=Depends(get_db)):
    return await UserController.update(user_id=user_id, user=user, db=db)

@protected_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session= Depends(get_db)):
    return await UserController.delete(user_id=user_id, db=db)

router.include_router(protected_router)