from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Bool(int, Enum):
    True = 1
    False = 0

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=30)
    email: str = Field(..., regex=r'^[\w\.\+\-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$', max_length=50)
    pwd: str = Field(..., max_length=60, max_length=60)
    lastPwd: Optional[str]  = None
    dtRegistration: datetime = None
    dtChangedPwd: Optional[datetime]
    userDisabled: Bool = False

    class Config:
        orm_mode = True


''' Definizione in SQLAlchemy
Base = declarative_base()

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    pwd = Column(String)
    lastPwd = Column(String)
    dtRegistration = Column(DateTime)
    dtChangedPwd = Column(DateTime)
    userDisabled = Column(Boolean)

    def __repr__(self):
        return f"<User {self.id} | {self.username} | {self.email}>"

'''