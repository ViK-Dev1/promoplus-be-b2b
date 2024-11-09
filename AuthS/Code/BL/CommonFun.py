
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from Config.appsettings import SATE_SERVICE_ACCESS_TOKEN_EXP, SKS_SECRETKEY_SERVICE
from Database.CommonQuery import GetQSelectUser


## common Functions

# check if the string passed is null or empty
def IsNullOrEmpyStr(tempStr: str) -> bool:
    if tempStr != None and tempStr != '':
        return False
    return True


# create a response for the specified status code and error message
def CreateErrorResponse(statusCode: str, errorMsg: str) -> HTTPException:
    return HTTPException(
        status_code = statusCode,
        detail= errorMsg
    )


#  get a the ID that identifies the current service
def GetServiceJWTToken(serviceName: str) -> bytes:
    if IsNullOrEmpyStr(SKS_SECRETKEY_SERVICE):
        raise RuntimeError('detail": "CONFIG KEY NOT FOUND: SKS')
    if IsNullOrEmpyStr(SATE_SERVICE_ACCESS_TOKEN_EXP):
        raise RuntimeError('detail": "CONFIG KEY NOT FOUND: SATE')
    sks = SKS_SECRETKEY_SERVICE
    sate = SATE_SERVICE_ACCESS_TOKEN_EXP
    tokenName = {
        "serviceName": serviceName
    }
    serviceJWTToken = GenerateToken(sks, sate, tokenName)

    '''
    sksB = sks.encode('utf-8') 
    serviceID = b''

    serviceNameB = serviceName.encode('utf-8') if isinstance(serviceName, str) else serviceName
    
    # Create the HMAC object
    hmac_object = hmac.new(sksB, serviceNameB, hashlib.sha256)
    
    # Get the digest
    serviceID_digest = hmac_object.digest()
    serviceID = serviceID_digest.hex()'''

    return serviceJWTToken

# generate JWT token
def GenerateToken(skJWTConfig: str, expTimeConfig, tokenBody: dict, expTimeScale = 'mm'):
    if expTimeScale == 'mm':
        expTimeConfig = expTimeConfig
    elif expTimeScale == 'hh':
        expTimeConfig = expTimeConfig *60

    at_expiry_delta = timedelta(minutes=expTimeConfig)
    to_encode = {
        "sub": tokenBody
    }
    expiry_dt = datetime.utcnow() + at_expiry_delta
    to_encode.update({"exp": expiry_dt})
    try:
        encoded_jwt = jwt.encode(to_encode, skJWTConfig, algorithm="HS256")
    except Exception as e1:
        RuntimeError('An error occurred while generating jwt token')
    return encoded_jwt

# Get user from DB
def get_user_fromDB(email: str, db: Session) -> list:
    query = GetQSelectUser({
        'email': email
    })
    try:
        res1 = db.execute(query.query, query.params).all()
        if len(res1) == 1:
            return res1
    except Exception as e1:
        raise RuntimeError('DB-Q error: SLogin / getUser')
    return []

# Send email asyncronously
