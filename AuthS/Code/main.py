# Main controller to manage all the endpoints within this service

from fastapi import Body, FastAPI, HTTPException, status, Depends, Header
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

# Request e Response
from Database.db import get_db
from ReqResModels.ReqLogin import ReqLogin

# Business logic
from BL import SLogin, SCheckToken


app = FastAPI()

#CONTROLLERS

## Public services
@app.post("/login")
async def login(request: ReqLogin = Body(), db: Session = Depends(get_db)):
    return SLogin.sLogin(request, db)

@app.post("/changePwd")
async def changePwd():
    return "ciaooo"
    
@app.post("/register")
async def register():
    return "ciaooo"

## Internal services
### mettere un controllo che verifica il servizio da cui proviene la request, metterlo dentro un hash corto 
@app.get("/ICIsTokenValid")
async def checkToken(token: str = Header()):
    return SCheckToken.sCheckToken(token)


# Requests handlers
## BAD REQUEST
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc):
    err1 = exc.errors()[0]
    errDetails = {}
    field1 = err1["loc"][1]
    errMsg1 = err1["msg"]
    errDetails["field"] = field1
    errDetails["message"] = errMsg1

    raise HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        detail={"errors":errDetails},
        headers={"Content-Type":"application/json"}
    )
