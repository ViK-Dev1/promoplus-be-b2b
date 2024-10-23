from datetime import datetime, timedelta
import bcrypt
from fastapi import Depends, HTTPException, status
import jwt.algorithms
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt


from Models.LogLoginActivity import LogLoginActivity
from Config.appsettings import UATE_USER_ACCESS_TOKEN_EXP
from Config.appsettings import LATP_LOGIN_ATTEMPT_TIME_PERIOD
from Config.appsettings import SKJWT_SECRETKEY_JWT
from Config.appsettings import SSP_SALT_SECRET_PWD
from BL.CommonFun import CreateErrorResponse, GenerateToken, IsNullOrEmpyStr
from Database.db import get_db

from ReqResModels.ReqLogin import ReqLogin
from ReqResModels.ResLogin import ResLogin

def sLogin(request: ReqLogin, db: Session):
    # calculate the hashed pwd
    hashedPwd = hash_pwd(request.password)
    
    # verify on db if the user exist (with username / email and pwd)
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
                   
        #Recupero il numero di tentativi errati dai logs
        loginAttempt = get_loginAttemptDB(usrFound.email, db)
        if(usrFound.pwd == hashedPwd):
            if(usrFound.userDisabled == 1):
                #utente disabilitato
                raise CreateErrorResponse(status.HTTP_401_UNAUTHORIZED, 
                                          "L'utenza indicata è stata disabilitata. Reimpostare la password o contattare l'assistenza per maggiori informazioni")
            else:
                #tutto ok, genero il token e consento l'accesso
                # jwt token = id, email
                if IsNullOrEmpyStr(SKJWT_SECRETKEY_JWT):
                    raise RuntimeError('CONFIG KEY NOT FOUND: SKJWT')
                skJWTConfig = SKJWT_SECRETKEY_JWT
                if IsNullOrEmpyStr(UATE_USER_ACCESS_TOKEN_EXP):
                    raise RuntimeError('CONFIG KEY NOT FOUND: UATE')
                expTimeConfig = UATE_USER_ACCESS_TOKEN_EXP
                tokenBody = {
                    'id': usrFound.id,
                    'email': usrFound.email
                }
                tokenJWT = GenerateToken(skJWTConfig, expTimeConfig, tokenBody)
                upd_loginAttemptLogs(True, 0, loginAttempt[1], usrFound.id, loginAttempt[1], db)
                return ResLogin(
                    username = usrFound.username,
                    email = usrFound.email,
                    registrationDT = usrFound.dtRegistration,
                    token = tokenJWT
                )
        else:
            #credenziali errate
            if(loginAttempt[0] == 0):
                #nell'ultimo TIMESPAN di monitoraggio dei login non ci sono state attività di login per questa utenza
                upd_loginAttemptLogs(False, 0, 1, usrFound.id, loginAttempt[2], db)
            else:
                if(loginAttempt[1] <= 5):
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
            upd_query = text('INSERT INTO AuthS.LogLoginActivity (userId, loginResult, dtLogin, attemptNum)'+
                             ' VALUES'+
                             ' (:userId, :loginResult, :dtLogin, :attemptNum)')
            upd_params = {
                'userId': userId,
                'loginResult': "OK" if loginOK else "WP",
                'dtLogin': now,
                'attemptNum': attemptNum
            }
        else:
            #aggiorno il record di log gia' presente (incremento loginAttempt e aggiorno l'orario)
            attemptNum += 0 if loginOK else 1
            attemptNum = 5 if attemptNum > 5 else attemptNum
            upd_query = text('UPDATE AuthS.LogLoginActivity'+
                             ' SET attemptNum = :attemptNum, loginResult = :loginResult, dtLogin = :dtLogin'+
                             ' WHERE id = :id')
            upd_params = {
                'id': logAttemptId,
                'attemptNum': attemptNum,
                'loginResult': "OK" if loginOK else "WP",
                'dtLogin': now
            }
        db.execute(upd_query, upd_params)
        db.commit()

        #aggiorno disabledUser nella tabella degli utenti
        if(attemptNum == 5 and loginOK == False):
            upd_query = text('UPDATE AuthS.Users'+
                             ' SET userDisabled = :userDisabled'+
                             ' WHERE id = :userId')
            upd_params = {
                'userId': userId,
                'userDisabled': 1
            }
            db.execute(upd_query, upd_params)
            db.commit()
        
    except Exception as e1:
        print(e1)
        raise RuntimeError('DB-Q error: SLogin / updLoginAttempt')


#ritorna il numero di login attempt sbagliati effettuati nell'ultima 1h dall'ultima login positiva
def get_loginAttemptDB(email: str, db: Session):
    if IsNullOrEmpyStr(LATP_LOGIN_ATTEMPT_TIME_PERIOD):
        raise RuntimeError('CONFIG KEY NOT FOUND: LATP')
    timeFrom = datetime.now() - timedelta(minutes=LATP_LOGIN_ATTEMPT_TIME_PERIOD)
    query = text('SELECT logslogin.id, logslogin.loginResult, logslogin.attemptNum' +
            ' FROM AuthS.Users AS usr' +
            ' INNER JOIN AuthS.LogLoginActivity AS logslogin ON logslogin.userId = usr.id' +
            '        AND usr.email = :email' +
            ' WHERE logslogin.dtLogin >= :timeFrom' +
            ' ORDER BY logslogin.dtLogin DESC' +
            ' LIMIT 1')
    
    q_params = {
        'email': email,
        'timeFrom': timeFrom
    } 
    ris = [0,0,0]
    try:
        res1 = db.execute(query, q_params).all()
        if len(res1) == 1 and res1[0][1] == 'WP':
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

class UsrData:
    def __init__(self, id, username, email, pwd, dtRegistration, userDisabled):
        self.id = id
        self.username = username
        self.email = email
        self.pwd = pwd
        self.dtRegistration = dtRegistration
        self.userDisabled = userDisabled

    id: int
    username: str
    email: str
    pwd: str
    dtRegistration: datetime
    userDisabled: int

def get_user_fromDB(email: str, db: Session) -> list:
    query = text('SELECT id, username, email, pwd, dtRegistration, userDisabled'+
                 ' FROM AuthS.Users AS a'+
                 ' WHERE a.email = :email'+
                 ' LIMIT 1')
    q_params = {
        'email': email
    } 
    try:
        res1 = db.execute(query, q_params).all()
        if len(res1) == 1:
            return res1
    except Exception as e1:
        raise RuntimeError('DB-Q error: SLogin / getUser')
    return []
