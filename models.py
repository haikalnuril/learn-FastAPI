from db_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import bcrypt


class ProjectStatus(str, enum.Enum):
    IN_PROGRESS = "on-progress"
    FINISHED = "finished"
    CANCELED = "canceled"

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)
    
    # Relationship with Project
    projects = relationship("Projects", back_populates="user")
    
    def set_password(self, password: str):
        # Hash the password
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def verify_password(self, password: str):
        password_bytes = password.encode('utf-8')
        hashed = self.password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed)

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)
    created_at = Column(DateTime, default=datetime)
    updated_at = Column(DateTime, default=datetime, onupdate=datetime)
    
    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship with User
    user = relationship("Users", back_populates="projects")