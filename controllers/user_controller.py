from typing import Any, Dict
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db_config import get_db
from models.user_model import CreateUserRequest, LoginUserRequest, UpdateUserRequest
from services.user_service import UserService


class UserController :
    @staticmethod
    async def create(user: CreateUserRequest, db: Session = Depends(get_db))-> Dict[str, Any]:
        try:
            users = await UserService.create(request=user, db=db)
            return {
                "message" : "User Created Successfully",
                "data": users
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
            
    @staticmethod
    async def login(request: LoginUserRequest, db: Session = Depends(get_db))-> Dict[str, Any]:
        try:
            users = await UserService.login(request=request, db=db)
            return {
                "message": "Login Successfully",
                "data": users
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
            
    @staticmethod
    async def update(user_id: int, user: UpdateUserRequest, db: Session= Depends(get_db))-> Dict[str, Any]:
        try:
            users = await UserService.update(user_id=user_id, request=user, db=db)
            return {
                "message": "User updated successfully",
                "data": users
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
            
    @staticmethod
    async def delete(user_id: int, db: Session= Depends(get_db)) -> Dict[str, Any]:
        try:
            users = await UserService.delete(user_id=user_id, db= db)
            
            if not users:
                return users
            return {
                "message": "User deleted successfully"
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )