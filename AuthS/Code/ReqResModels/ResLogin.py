from pydantic import BaseModel, Field
from datetime import datetime

## Response
class ResLogin(BaseModel):
    username: str
    email: str
    registrationDT: datetime
    token: str