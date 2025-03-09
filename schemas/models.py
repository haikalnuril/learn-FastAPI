from db_config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum


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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship with Project
    projects = relationship("Projects", back_populates="user")

class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.IN_PROGRESS)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship with User
    user = relationship("Users", back_populates="projects")