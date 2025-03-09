from sqlalchemy.orm import Session

from models.user_model import CreateUserRequest
from passlib.context import CryptContext
from schemas import Users


pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService :
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
        
        return db_user