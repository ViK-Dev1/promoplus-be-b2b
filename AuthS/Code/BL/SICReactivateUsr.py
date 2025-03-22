from sqlalchemy.orm import Session
from BL.CommonFun import get_user_fromDB
from fastapi import Response, status
from Database.QuerySICReactivateUsr import GetQUpdateReactivateUser
from ReqResModels.ReqUserData import ReqUserData

# Riattiva l'utenza dell'utente di cui si indica la mail
def sICReactivateUsr(request: ReqUserData, db: Session):
    #search the user
    usrFound1 = get_user_fromDB(request.email, db)
    if len(usrFound1) == 1:
        #utente trovato
        usrFound = UsrData(
            usrFound1[0][0],
            usrFound1[0][1],
            usrFound1[0][2],
            usrFound1[0][3].encode('utf-8'),
            usrFound1[0][4],
            usrFound1[0][5]
        )
        # Just when it is disabled (val>0) I'll reactivate it by setting val=0
        if(usrFound.userDisabled != 0):
            #vado a riattivarlo
            try:
                query = GetQUpdateReactivateUser({
                    'userId': usrFound.id
                })
                db.execute(query.query, query.params)
                db.commit()
            except Exception as e1:
                raise RuntimeError('DB-Q error: SICReactivateUsr / updReactivateUser')
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND) #errore utente non trovato