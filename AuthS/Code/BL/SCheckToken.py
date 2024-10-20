from fastapi import status

import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from ReqResModels.ResICIsTokenValid import ResICIsTokenValid
from Config.appsettings import SKJWT_SECRETKEY_JWT
from BL.CommonFun import CreateErrorResponse, IsNullOrEmpyStr

def sCheckToken(token: str):
    try:
        if(len(token.split(' ')) == 2):
            tknLst = token.split(' ')
            if(tknLst[0] == 'Bearer'):
                tkn = tknLst[1]
                if IsNullOrEmpyStr(SKJWT_SECRETKEY_JWT):
                    raise RuntimeError('CONFIG KEY NOT FOUND: SKJWT')
                skjwt = SKJWT_SECRETKEY_JWT
                try:
                    payload = jwt.decode(tkn, skjwt, algorithms=["HS256"])
                except (Exception, ExpiredSignatureError, InvalidSignatureError) as decodeExcp:
                    #print(decodeExcp) #<----- per verificare perchè non è valido decommentare
                    raise CreateErrorResponse(status.HTTP_401_UNAUTHORIZED, "Invalid token")
                userId = payload.get("sub")["id"]
                if userId is not None and userId > 1:
                    return ResICIsTokenValid(userId=userId)
        raise CreateErrorResponse(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    except RuntimeError as e:
        if e is not dict:
            raise CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, e.__str__())