from pydantic import BaseModel, Field
from typing import Optional

## Request
class ReqUserData(BaseModel):
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', min_length=5, max_length=30)
    newEmail: Optional[str] = Field(default=None, pattern=r'^[a-zA-Z0-9._%+-]{2,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', min_length=5, max_length=30)
    newUsername: Optional[str] = Field(default=None, pattern=r'^\S+$', min_length=5, max_length=30)
    confirmToken: Optional[str] = Field(default=None)