# Main controller to manage all the endpoints within this service

from http.client import HTTPResponse
import sys
from fastapi import Body, FastAPI, HTTPException, status, Depends, Header
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
import uvicorn

# Request e Response
from BL.CommonFun import CreateErrorResponse, GetServiceJWTToken
from Database.db import get_db
from Middleware.AuthCheckMiddleware import AuthCheckMiddleware
from Middleware.ICAuthCheckMiddleware import ICAuthCheckMiddleware
from ReqResModels.ReqLogin import ReqLogin

# Business logic
from BL import ProtectedRoutes, SLogin

app = FastAPI(openapi_url=None)
protectedRoutes = ProtectedRoutes.ProtectedRoutes()
serviceName = 'AuthS'
serviceID = ''

# MIDDLEWARE
## l'ordine in cui vengono controllati: da quello più in basso a quello più in alto

## 2. ICAuthCheck - applied to routes for internal communication
app.add_middleware(ICAuthCheckMiddleware, protectedRoutes = protectedRoutes.icProtectedRoutes)

## 1. AuthCheckMiddleware - applied to routes that require authentication
app.add_middleware(AuthCheckMiddleware, protectedRoutes = protectedRoutes.authProtectedRoutes)

#CONTROLLERS

## Public services
@app.post("/login")
async def login(request: ReqLogin = Body(), db: Session = Depends(get_db)):
    return SLogin.sLogin(request, db)
    
@app.post("/register")
async def register():
    return "ciaooo"

@app.post("/changePwd")
async def changePwd():
    return "ciaooo"

@app.post("/ICChangeUsr")
async def changeUsr():
    return "ICChangeUsr funziona"

@app.post("/ICChangeEmail")
async def changeEmail():
    return "ICChangeEmail funziona"

# Common errors handlers
## BAD REQUEST
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc):
    err1 = exc.errors()[0]
    errDetails = {}
    field1 = err1["loc"][1]
    errMsg1 = err1["msg"]
    errDetails["field"] = field1
    errDetails["message"] = errMsg1

    raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, errDetails)

## SERVER SIDE ERROR
@app.exception_handler(RuntimeError)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())


def main():
    #int(sys.argv[1])
    #check important configurations
    #serviceName = sys.argv[2]
    try:
        serviceID = GetServiceJWTToken(serviceName)
    except RuntimeError as e1:
        print(f' | Service: {serviceName} | '+e1.__str__())
        return
    print(f' | Service: {serviceName} | {serviceID}')
    #start the server
    uvicorn.run(app, host="0.0.0.0", port=8001)#int(sys.argv[1]))

if __name__ == "__main__":
    main()