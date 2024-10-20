
from fastapi import HTTPException


def IsNullOrEmpyStr(tempStr: str) -> bool:
    if tempStr != None and tempStr != '':
        return False
    return True

def CreateErrorResponse(statusCode: str, errorMsg: str) -> HTTPException:
    return HTTPException(
        status_code = statusCode,
        detail= errorMsg,
        headers={"Content-Type":"application/json"}
    )