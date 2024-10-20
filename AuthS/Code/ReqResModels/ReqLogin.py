from pydantic import BaseModel, Field

## Request
class ReqLogin(BaseModel):
    email: str = Field(..., min_length=5, max_length=30)
    password: str = Field(..., min_length=8, max_length=30)
