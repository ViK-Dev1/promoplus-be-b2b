
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
from sqlalchemy.orm import Session
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from cryptography.hazmat.primitives import serialization
import os

from Config.appsettings import (
    SATE_SERVICE_ACCESS_TOKEN_EXP, SKS_SECRETKEY_SERVICE, 
    PrivateK_JWT_FileName, PublicK_JWT__FileName,
    CONFIG_FLD    
)
from Database.CommonQuery import GetQSelectUser

#JWT token manager (singleton)
class JWTTokenKeysManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(JWTTokenKeysManager, cls).__new__(cls, *args, **kwargs)
            
            cwd = os.getcwd()
            cwd = cwd+'\\'+cls._instance.GetConfigFolder()
            print(cwd)

            cls._instance.privateKey = ''  # private key vuota
            cls._instance.publicKey = ''   # public key vuota
            cls.ReadPrivateKey(cls._instance, cwd)
            cls.ReadPublicKey(cls._instance, cwd)
            # Test effettuato e viene correttamente letto solo una volta da file
            # poi si recuperano queste info dall'istanza già creata
            print('- -- --- ---- JWT TKN MANAGER creato ---- --- -- -')
        return cls._instance

    def GetConfigFolder(self) -> str:
        if IsNullOrEmpyStr(CONFIG_FLD):
            raise RuntimeError('detail": "CONFIG KEY NOT FOUND: CONFIG_FLD')
        return CONFIG_FLD

    def ReadPrivateKey(self, configPath):
        '''
        Carica la private key dal file
        '''
        self.privateKey = ""
        if IsNullOrEmpyStr(PrivateK_JWT_FileName):
            raise RuntimeError('detail": "CONFIG KEY NOT FOUND: PrivateK_JWT_FileName')
        with open(configPath+'\\'+PrivateK_JWT_FileName, "rb") as key_file:
            self.privateKey = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

    def ReadPublicKey(self, configPath):
        '''
        Carica la public key dal file
        '''
        self.publicKey = ""
        if IsNullOrEmpyStr(PublicK_JWT__FileName):
            raise RuntimeError('detail": "CONFIG KEY NOT FOUND: PublicK_JWT__FileName')
        with open(configPath+'\\'+PublicK_JWT__FileName, "rb") as key_file:
            self.publicKey = serialization.load_pem_public_key(
                key_file.read(),
            )

    def GetPrivateKey(self) -> str:
        return self.privateKey
    
    def GetPublicKey(self) -> str:
        return self.publicKey

## common Functions

def IsNullOrEmpyStr(tempStr: str) -> bool:
	"""
	Controlla se la stringa passata è vuota o None / null
	"""
	if tempStr != None and tempStr != '':
		return False
	return True

def CreateErrorResponse(statusCode: str, errorMsg: str) -> HTTPException:
	"""
	Crea una response per con il messaggio e status code indicato
	"""
	return HTTPException(
		status_code = statusCode,
		detail= errorMsg
	)

def GetServiceJWTToken(serviceName: str) -> bytes:
    """
    Ritorna un token JWT che identifica il servizio corrente
    """   
    sate = SATE_SERVICE_ACCESS_TOKEN_EXP
    tokenName = {
        "serviceName": serviceName
    }
    serviceJWTToken = GenerateToken(sate, tokenName)

    return serviceJWTToken

def GenerateToken(expTimeConfig, tokenBody: dict, expTimeScale = 'mm'):
    """
    Genera un token JWT
    """
    jwtTKNManager = JWTTokenKeysManager()
    pvtKey = jwtTKNManager.GetPrivateKey()
    if jwtTKNManager == None or IsNullOrEmpyStr(pvtKey):
        raise RuntimeError('detail": "jwtTKNManager error')
    
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
    encoded_jwt = ''
    try:
        encoded_jwt = jwt.encode(to_encode, pvtKey, algorithm="RS256")
    except Exception as e1:
        RuntimeError('An error occurred while generating jwt token')
    return encoded_jwt

def get_user_fromDB(email: str, db: Session) -> list:
    """
    Ritorna l'utente con l'email che viene indicata
    """
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
