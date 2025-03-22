from sqlalchemy.orm import Session
from BL.CommonFun import GenerateToken, IsNullOrEmpyStr, get_user_fromDB
from fastapi import Response, status
from fastapi.responses import JSONResponse
from Config.appsettings import SKCE_SECRETKEY_CONFEMAIL, CETE_CONFEMAIL_TOKEN_EXP
from ReqResModels.ReqUserData import ReqUserData

# Sends an email to confirm the email to use for the registration
def sConfirmEmail(request: ReqUserData, db: Session):

    if(request.email == None
       or request.email == ''
       or request.email.strip() == ''):
        return JSONResponse(
            content={"details": "Non e' stata fornita una nuova email valida"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

    #search the user
    usrFound1 = get_user_fromDB(request.email, db)
    if len(usrFound1) == 1:
        #utente trovato -> utente già registrato -> loggarsi
        return JSONResponse(
            content={"details": "L'email indicata e' già stata registrata da un altro utente. Registrarsi con una nuova email o effettuare il login."},
            status_code=status.HTTP_409_CONFLICT
        )
    else:
        if IsNullOrEmpyStr(SKCE_SECRETKEY_CONFEMAIL):
                raise RuntimeError('CONFIG KEY NOT FOUND: SKCE')
        skey = SKCE_SECRETKEY_CONFEMAIL
        if IsNullOrEmpyStr(CETE_CONFEMAIL_TOKEN_EXP):
                raise RuntimeError('CONFIG KEY NOT FOUND: CETE')
        expTime = CETE_CONFEMAIL_TOKEN_EXP
        tknBody = {
            "email": request.email
        }
        token = GenerateToken(skey, expTime, tknBody, expTimeScale='hh')
        #inviare email
         #>ok inviata
         #>errore
        return "miao"