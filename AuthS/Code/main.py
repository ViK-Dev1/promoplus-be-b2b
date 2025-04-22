# Main controller to manage all the endpoints within this service

# region Import di librerie e tool
from http.client import HTTPResponse
import sys
import MySQLdb
import anyio
from fastapi import Body, Response, FastAPI, HTTPException, status, Depends, Header, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import sqlalchemy
from sqlalchemy.orm import Session
import uvicorn
# endregion

# region Import: middleware, BL, db, request & response
from BL import BLLogin
from Database.db import get_db
from Middleware.AdminCheckMiddleware import AdminCheckMiddleware
from Middleware.AuthCheckMiddleware import AuthCheckMiddleware
from Middleware.ICAuthCheckMiddleware import ICAuthCheckMiddleware
from Middleware.ErrorHandlerMiddleware import ErrorHandlerMiddleware
from ReqResModels.ReqLogin import ReqLogin
from ReqResModels.ReqUserData import ReqUserData
from BL import ProtectedRoutes, SConfirmEmail, SICChangeUsrData, SICReactivateUsr, BLCheckSDB
from BL.CommonFun import CreateErrorResponse, GetServiceJWTToken, LoggingManager
# endregion

app = FastAPI(openapi_url=None)
protectedRoutes = ProtectedRoutes.ProtectedRoutes()
serviceName = 'AuthS'
serviceID = ''


# region MIDDLEWARE
## Associazione dei middleware con il controller API principale
## L'ordine in cui vengono controllati: da quello più in basso a quello più in alto

## 4. ErrorHandlerMiddleware - capture any error / exception that might occur while executing middleware code before BL
app.add_middleware(ErrorHandlerMiddleware)

## 3. [A] - AdminCheckMiddleware - checks if the user who is calling is an admin
# non necessario qui
# app.add_middleware(AdminCheckMiddleware, protectedRoutes = protectedRoutes.adminProtectedRoutes)

## 2. [IC] - ICAuthCheckMiddleware - applied to routes for internal communication
app.add_middleware(ICAuthCheckMiddleware, protectedRoutes = protectedRoutes.icProtectedRoutes)

## 1. [L] - AuthCheckMiddleware - applied to routes that require authentication
# non necessario qui
# app.add_middleware(AuthCheckMiddleware, protectedRoutes = protectedRoutes.authProtectedRoutes)
# endregion

# region CONTROLLERS
## [A] - Endpoint per amministratori
@app.get("/checkS") #ok
async def checkS():
    return Response(status_code=status.HTTP_200_OK)

@app.get("/checkSDB") #ok
async def checkSDB(db: Session = Depends(get_db)):
    return BLCheckSDB.checkSDB(db)

## [P] - Endpoint pubblici
@app.post("/login") #ok
async def login(background_tasks: BackgroundTasks, request: ReqLogin = Body(), db: Session = Depends(get_db)):
    return BLLogin.login(request, db, background_tasks)

@app.post("/sendChangePwdLink") #da fare
async def sendChangePwdLink():
    return "sendChangePwdLink ok"

@app.post("/changePwd") #da fare
async def changePwd():
    return "changePwd ok"


## [IC] - Internal Communication services
@app.get("/provaIC") #da fare
async def provaIC():
    return "provaIC ok"

@app.post("/ICRegisterUsers") #da fare
async def icRegisterUsers(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICReactivateUsr.sICReactivateUsr(request, db)

@app.post("/ICChangeUsrData") #da fare
async def ICChangeUsrData(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICChangeUsrData.sICChangeUsrData(request, db)

@app.post("/ICReactivateUsr") #da fare
async def changeUsr(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICReactivateUsr.sICReactivateUsr(request, db)

@app.post("/ICChangeUsrData") #da fare
async def ICChangeUsrData(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICChangeUsrData.sICChangeUsrData(request, db)

@app.post("/ICReactivateUsr") #da fare
async def changeUsr(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICReactivateUsr.sICReactivateUsr(request, db)

@app.post("/ICChangeUsrData") #da fare
async def ICChangeUsrData(request: ReqUserData = Body(), db: Session = Depends(get_db)):
    return SICChangeUsrData.sICChangeUsrData(request, db)
# endregion 

# region Common errors handlers
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
@app.exception_handler(sqlalchemy.exc.OperationalError)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(MySQLdb.OperationalError)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(RuntimeError)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())    
@app.exception_handler(IndexError)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(Exception)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(TypeError)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(anyio.WouldBlock)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
@app.exception_handler(anyio.EndOfStream)
async def serverError_handler(req, exc):
    if exc is not dict:
        LoggingManager().error(f"Server error | {exc.__str__()}")
        raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, exc.__str__())
# endregion 

'''
Per startare numerose istanze decommentare le righe commentate e chiamare il main indicando come argomento la porta
'''
def main():
    #int(sys.argv[1])
    #check important configurations
    #serviceName = sys.argv[2]
    try:
        serviceID = GetServiceJWTToken(serviceName)
    except (RuntimeError, UnboundLocalError) as e1:
        #print(f' | Service: {serviceName} | '+e1.__str__())
        return
    #print(f' | Service: {serviceName} | {serviceID}')
    #start the server
    uvicorn.run(app, host="0.0.0.0", port=8081) #int(sys.argv[1]))
    # implementare un meccanismo che dal 55esimo minuto venga generato un nuovo token per il servizio e si inizi ad usare quello

if __name__ == "__main__":
    main()