from MySQLdb import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends, HTTPException, status, Response

from BL.CommonFun import CreateErrorResponse, JWTTokenKeysManager

def checkSDB(db: Session):
    q1 = text('SELECT 1;')
    res1 = db.execute(q1)
    if res1 != None:
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)