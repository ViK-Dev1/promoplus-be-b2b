from datetime import datetime, timedelta
import bcrypt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt

from Models.Constants import WRONG_PWD, CHG_PWD
from Config.appsettings import (
    ULTE_USER_LOGIN_TOKEN_EXP, LATP_LAST_ATTEMPT_TIME_PERIOD,
    SSP_SALT_SECRET_PWD, CPP_CHANGE_PWD_PERIOD
)
from BL.CommonFun import (
    CreateErrorResponse, GenerateToken, 
    IsNullOrEmpyStr, get_user_fromDB
)
from Database.db import get_db

from Models.UserData import UserData
from ReqResModels.ReqLogin import ReqLogin
from ReqResModels.ResLogin import ResLogin, UsrData1

# DB Query for this service
from Database.QuerySLogin import GetQInsertLogLoginRecord
from Database.QuerySLogin import GetQUpdateLogLoginRecord
from Database.QuerySLogin import GetQUpdateDisableUser
from Database.QuerySLogin import GetQSelectWrongLoginAttempts

def login(request: ReqLogin, db: Session):
    # calculate the hashed pwd
    hashedPwd = hash_pwd(request.password)
    
    # verify on db if the user exist (with username / email and pwd)
    usrFound1 = get_user_fromDB(request.email, db)

    if len(usrFound1) == 1:
        #utente trovato
        usrFound = UserData(
            id=usrFound1[0][0], 
            username=usrFound1[0][1], 
            email=usrFound1[0][2], 
            pwd=usrFound1[0][3].encode('utf-8'),
            dtPwdChanged=usrFound1[0][4],  
            dtRegistration=usrFound1[0][5],
            pwdExpired=usrFound1[0][6],
            userDisabledPwd=usrFound1[0][7],
            userDisabled=usrFound1[0][8],
            usabilityTime=usrFound1[0][9], 
            usabilityDays=usrFound1[0][10] 
        )
                   
        #Recupero il numero di tentativi errati dai logs
        loginAttempt = get_loginAttemptDB(usrFound.id, db)
        if(usrFound.pwd == hashedPwd):
            if(usrFound.userDisabled == 1 or
               usrFound.userDisabledPwd == 1):
                #utente disabilitato
                raise CreateErrorResponse(status.HTTP_401_UNAUTHORIZED, 
                                          "L'utenza indicata è stata disabilitata. Reimpostare la password o contattare l'assistenza per maggiori informazioni")
            else:
                #tutto ok, genero il token e consento l'accesso
                # jwt token = id, email, username
                if IsNullOrEmpyStr(ULTE_USER_LOGIN_TOKEN_EXP):
                    raise RuntimeError('CONFIG KEY NOT FOUND: ULTE')
                expTimeConfig = ULTE_USER_LOGIN_TOKEN_EXP
                tokenBody = {
                    'id': usrFound.id,
                    'email': usrFound.email,
                    'username': usrFound.username
                }
                tokenJWT = GenerateToken(expTimeConfig, tokenBody)
                # se la password è scaduta o è passato più del numero di giorni 
                # indicati nella chiave di config
                # imposto nelle requiredActions di cambiare la password
                requiredActions = []
                if IsNullOrEmpyStr(CPP_CHANGE_PWD_PERIOD):
                    raise RuntimeError('CONFIG KEY NOT FOUND: CPP')
                cpp = int(CPP_CHANGE_PWD_PERIOD)
                changePwdRequired = False
                if usrFound.dtPwdChanged != None:
                    changePwdDay = usrFound.dtPwdChanged + timedelta(days=cpp)
                    if datetime.now() >= changePwdDay:
                        changePwdRequired = True
                if(usrFound.pwdExpired == 1 or changePwdRequired):
                    requiredActions.append(CHG_PWD)
                upd_loginAttemptLogs(True, 0, loginAttempt[1], usrFound.id, loginAttempt[1], db)
                res_usrdata1 = UsrData1(
                    usrFound.username, usrFound.email,
                    usrFound.dtPwdChanged, usrFound.dtRegistration,
                    usrFound.usabilityTime, usrFound.usabilityDays
                )
                return ResLogin(
                    userData = res_usrdata1,
                    token = tokenJWT,
                    requiredAction = requiredActions
                )
        else:
            #credenziali errate
            if(loginAttempt[0] == 0):
                #nell'ultimo TIMESPAN di monitoraggio dei login non ci sono state attività di login per questa utenza
                upd_loginAttemptLogs(False, 0, 1, usrFound.id, loginAttempt[2], db)
            else:
                if(loginAttempt[1] <= 5): #se ho già fatto 4 tentativi sbagliati, segno anche il 5°, poi non segno più
                    upd_loginAttemptLogs(False, loginAttempt[0], loginAttempt[1], usrFound.id, loginAttempt[2], db)
                if(loginAttempt[1] >= 4):
                    #numero di accessi errati superato
                    raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, "La sua utenza e' stata disabilitata per numerosi tentativi di accesso! Reimpostare la password o chiedere aiuto all'assistenza")
            raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, "Le credenziali inserite sono errate")
    else:
        #Utente non trovato
        raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, "Utenza non registrata! Per effettuare il login è necessario registrarsi")

def upd_loginAttemptLogs(loginOK: bool, logAttemptId: int, attemptNum: int, userId: int, prevLoginResult: str, db: Session):
    now = datetime.now()
    try:
        if(logAttemptId == 0 or prevLoginResult == 'OK'):
            #creo un nuovo record di log
            query = GetQInsertLogLoginRecord({
                'userId': userId,
                'loginOK': loginOK,
                'now': now,
                'attemptNum': attemptNum
            })
        else:
            #aggiorno il record di log gia' presente (incremento loginAttempt e aggiorno l'orario)
            attemptNum += 0 if loginOK else 1
            attemptNum = 5 if attemptNum > 5 else attemptNum
            query = GetQUpdateLogLoginRecord({
                'logAttemptId': logAttemptId,
                'attemptNum': attemptNum,
                'loginOK': loginOK,
                'now': now
            })
        db.execute(query.query, query.params)
        db.commit()

        #aggiorno disabledUser nella tabella degli utenti
        if(attemptNum == 5 and loginOK == False):
            query = GetQUpdateDisableUser({
                'userId': userId
            })
            db.execute(query.query, query.params)
            db.commit()
        
    except Exception as e1:
        raise RuntimeError('DB-Q error: SLogin / updLoginAttempt')


# Ritorna il numero di login attempt sbagliati effettuati nell'ultima 1h dall'ultima login positiva
# o in base al tempo indicato dalle configurazioni
def get_loginAttemptDB(idUsr: int, db: Session):
    if IsNullOrEmpyStr(LATP_LAST_ATTEMPT_TIME_PERIOD):
        raise RuntimeError('CONFIG KEY NOT FOUND: LATP')
    timeFrom = datetime.now() - timedelta(minutes=LATP_LAST_ATTEMPT_TIME_PERIOD)
    query = GetQSelectWrongLoginAttempts({
        'idUsr': idUsr,
        'timeFrom': timeFrom
    })
    ris = [0,0,0]
    try:
        res1 = db.execute(query.query, query.params).all()
        if len(res1) == 1 and res1[0][1] == WRONG_PWD:
            ris[0] = res1[0][0] #id
            ris[1] = res1[0][2] #attemptNumber
            ris[2] = res1[0][1] #loginResult
    except Exception as e1:
        raise RuntimeError('DB-Q error: SLogin / getLoginAttempt')
    return ris

def log_loginAttempt(userId: int, loginRes: str, attempNum: int):
    return ""

def hash_pwd(pwd: str):
    if IsNullOrEmpyStr(SSP_SALT_SECRET_PWD):
        raise RuntimeError('CONFIG KEY NOT FOUND: SSP')
    salt = SSP_SALT_SECRET_PWD.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), salt)
    hashed_FL_pwd = hashed_pwd.ljust(60, b'\0')
    return hashed_FL_pwd

def check_pwd(pwd2, hashed_pwd1) -> bool:
    bc_pwd2 = pwd2.encode('utf-8')
    if bcrypt.checkpw(bc_pwd2, hashed_pwd1):
        return True
    return False