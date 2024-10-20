from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class LoginResult(str, Enum):
    OK = "OK"
    WP = "PW"

class LogLoginActivity(BaseModel):
    id: int
    userId: int
    loginResult: Optional[LoginResult] = None
    dtLogin: datetime
    attemptNum: Optional[int] = 0
    token: Optional[str] = Field(..., min_length=255, max_length=255)
