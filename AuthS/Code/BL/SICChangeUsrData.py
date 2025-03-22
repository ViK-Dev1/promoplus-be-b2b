from sqlalchemy.orm import Session
from BL.CommonFun import CreateErrorResponse, get_user_fromDB
from fastapi import Response, status
from fastapi.responses import JSONResponse
from Database.QuerySICChangeUsr import GetQUpdateUsr
from ReqResModels.ReqUserData import ReqUserData

# Consente di modificare username o email all'utente di cui viene indicato il campo mail
def sICChangeUsrData(request: ReqUserData, db: Session):
    bannedWords = ['admin','god','madonna','dio','stronzo','merda','shit','porca','puttana','bitch']

    #checks if a username was provided
    if(request.newUsername == None
       or request.newUsername == ''
       or request.newUsername.strip() == ''):
        return JSONResponse(
            content={"details": "Non e' stato fornito un nuovo username valido"},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    if(IsWordPresent(request.newUsername.lower(), bannedWords)):
        return JSONResponse(
            content={"details": "Il nuovo username contiene alcune parole vietate. Scegliere un nuovo username"},
            status_code=status.HTTP_400_BAD_REQUEST
        )

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

        # Update username
        if request.newUsername != usrFound.username:
            try:
                query = GetQUpdateUsr({
                    'userId': usrFound.id,
                    'username': request.newUsername
                })
                db.execute(query.query, query.params)
                db.commit()
            except Exception as e1:
                raise RuntimeError('DB-Q error: SICChangeUsr / updUsr')
        
        #se presente anche una nuova email
        ## generare un token jwt da mettere in un token
        ## con email vecchia, nuova e expiry 1 giorno e inviarlo via mail e mandare 200
        ## altrimenti mandare un errore opportuno

        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND) #errore utente non trovato
    
def IsWordPresent(longWord:str, wordList: list) -> bool:
    res = False
    for wordToCheck in wordList:
        if wordToCheck in longWord:
            res = True
            break
    return res