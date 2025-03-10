from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user_model import CreateUserRequest, LoginUserRequest, UpdateUserRequest, toLoginUserResponse, toUserResponse
from passlib.context import CryptContext
from schemas import Users
from utils.JWT import JWT_token


pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService :
    @staticmethod
    async def getUserById(user_id: int, db: Session)->Optional[Users]:
        try:
            return db.query(Users).filter(Users.id == user_id).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user"
            )
            
    @staticmethod
    async def getUserByEmail(email: str, db: Session)-> Optional[Users]:
        try:
            return db.query(Users).filter(Users.email == email).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user by email"
            )
            
    @staticmethod
    async def getUserByUsername(username:str, db:Session)-> Optional[Users]:
        try:
            return db.query(Users).filter(Users.username == username).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user by username"
            )
    
    @staticmethod
    async def create(request: CreateUserRequest, db: Session) -> Users:
        request.password = pass_context.hash(request.password)
        
        db_user = Users(
            username=request.username,
            email=request.email,
            password=request.password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return toUserResponse.model_validate(db_user)
    
    @staticmethod
    async def login(request: LoginUserRequest, db: Session) -> Users:
        db_user = await UserService.getUserByEmail(request.email, db)
        
        if not db_user:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Password is wrong!"
        )
            
        verify_password = pass_context.verify(request.password, db_user.password)
        
        if not verify_password:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Password is wrong!"
        )
            
        token = JWT_token(
            data={
                "id": db_user.id,
                "username": db_user.username,
                "email":db_user.email
            }
        )
        
        user_response = toLoginUserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            token=token
        )
        return user_response
    
    @staticmethod
    async def update(user_id: int, request: UpdateUserRequest, db: Session) -> Users:
        
        db_user = await UserService.getUserById(user_id, db)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exist"
            )
        
        update_data = request.model_dump(exclude_unset=True)
        
        if "username" in update_data and update_data["username"] != db_user.username:
            exist_user = await UserService.getUserByUsername(update_data["username"], db)
            if exist_user:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username already taken by another user"
                    )
        
        if "password" in update_data:
            update_data["password"] = pass_context.hash(update_data["password"])
            
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        db.commit()
        db.refresh(db_user)
        return toUserResponse.model_validate(db_user)
    
    @staticmethod
    async def delete(user_id: int, db: Session) -> Users:
        
        db_user = await UserService.getUserById(user_id, db)
        
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exist"
            )
            
        db.delete(db_user)
        db.commit()
        
        return True