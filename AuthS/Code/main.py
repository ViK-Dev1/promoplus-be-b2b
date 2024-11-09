# Main controller to manage all the endpoints within this service

from http.client import HTTPResponse
import sys
import anyio
from fastapi import Body, FastAPI, HTTPException, status, Depends, Header
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
import uvicorn

# Request e Response
from BL.CommonFun import CreateErrorResponse, GetServiceJWTToken
from Database.db import get_db
from Middleware.AdminCheckMiddleware import AdminCheckMiddleware
from Middleware.AuthCheckMiddleware import AuthCheckMiddleware
from Middleware.ICAuthCheckMiddleware import ICAuthCheckMiddleware
from Middleware.ErrorHandlerMiddleware import ErrorHandlerMiddleware
from ReqResModels.ReqLogin import ReqLogin
from ReqResModels.ReqUserData import ReqUserData

# Business logic
from BL import ProtectedRoutes, SConfirmEmail, SICChangeUsrData, SLogin, SICReactivateUsr, SICChangeEmail

app = FastAPI(openapi_url=None)
protectedRoutes = ProtectedRoutes.ProtectedRoutes()
serviceName = 'AuthS'
serviceID = ''

# MIDDLEWARE
## l'ordine in cui vengono controllati: da quello più in basso a quello più in alto

## 4. ErrorHandlerMiddleware - capture any error / exception that might occur while executing middleware code before BL
app.add_middleware(ErrorHandlerMiddleware)

## 3. AdminCheckMiddleware - checks if the user who is calling is an admin
app.add_middleware(AdminCheckMiddleware, protectedRoutes = protectedRoutes.adminProtectedRoutes)

## 2. ICAuthCheckMiddleware - applied to routes for internal communication
app.add_middleware(ICAuthCheckMiddleware, protectedRoutes = protectedRoutes.icProtectedRoutes)

## 1. AuthCheckMiddleware - applied to routes that require authentication
app.add_middleware(AuthCheckMiddleware, protectedRoutes = protectedRoutes.authProtectedRoutes)

#CONTROLLERS

## Public services
@app.post("/confirmEMail") #da fare
async def confirmEmail(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SConfirmEmail.sConfirmEmail(request, db)

@app.post("/register") #da fare
async def register():
    return "ciaooo"

@app.post("/login") #ok
async def login(request: ReqLogin = Body(), db: Session = Depends(get_db)):
    return SLogin.sLogin(request, db)

@app.post("/changePwd") #da fare
async def changePwd():
    return "ciaooo"

@app.post("/confirmOP-A1") #da fare


## Internal Communication services
@app.post("/ICReactivateUsr") #ok
async def changeUsr(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICReactivateUsr.sICReactivateUsr(request, db)

@app.post("/ICChangeUsrData") #da fare
async def ICChangeUsrData(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICChangeUsrData.sICChangeUsrData(request, db)

# Common errors handlers
## BAD REQUEST
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req, exc):
    err1 = exc.errors()[0]
    errDetails = {}
    field1 = err1["loc"][1]
    errMsg1 = err1["msg"]
    errDetails["field"] = field1
    if 'email' in str(field1).lower() and 'pattern' in errMsg1:
        errMsg1 = 'Il valore inserito ha un formato non valido'
    if 'username' in str(field1).lower() and 'pattern' in errMsg1:
        errMsg1 = "Il valore inserito non puo' contenere spazi"
        
    errDetails["message"] = errMsg1

    raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, errDetails)

## SERVER SIDE ERROR
@app.exception_handler(RuntimeError)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())    
@app.exception_handler(IndexError)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(Exception)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(TypeError)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(anyio.WouldBlock)
async def serverError_handler(req, exc):
    if exc is not dict:
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(anyio.EndOfStream)
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