from datetime import datetime, timedelta
import bcrypt
from fastapi import Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
import jwt

from BL.BLEmails import EMailClient
from Models.Constants import (
    USR_NORMALE, WRONG_PWD, CHG_PWD
)
from Config.appsettings import (
    ULTE_USER_LOGIN_TOKEN_EXP, LATP_LAST_ATTEMPT_TIME_PERIOD,
    SSP_SALT_SECRET_PWD, CPP_CHANGE_PWD_PERIOD
)
from BL.CommonFun import (
    CreateErrorResponse, CreateErrorResponseHttp, GenerateToken, 
    IsNullOrEmpyStr, get_user_fromDB
)
from Database.db import get_db

from Models.UserData import UserData
from ReqResModels.ReqLogin import ReqLogin
from ReqResModels.ResLogin import ResLogin, UsrData1

# DB Query for this service
from Database.QuerySLogin import (
    GetQUpdSaveToken, GetQInsertLogLoginRecord,
    GetQUpdateLogLoginRecord, GetQUpdateDisableUser, 
    GetQSelectWrongLoginAttempts
)

def login(request: ReqLogin, db: Session, background_tasks: BackgroundTasks):
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
            userType=usrFound1[0][3],
            pwd=usrFound1[0][4].encode('utf-8'),
            dtPwdChanged=usrFound1[0][5],  
            dtRegistration=usrFound1[0][6],
            pwdExpired=usrFound1[0][7],
            userDisabledPwd=usrFound1[0][8],
            userDisabled=usrFound1[0][9],
            usabilityTime=usrFound1[0][10], 
            usabilityDays=usrFound1[0][11] 
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
                '''
                In base allo userType verifico se è possibile consentire l'accesso al sistema o meno
                e se necessario verificare l'orario di lavoro dell'utente considerato
                '''
                if(usrFound.userType == USR_NORMALE):
                    orarioLoginValido = check_orarioLogin(usrFound.usabilityTime, usrFound.usabilityDays)
                    if orarioLoginValido == False:
                        raise CreateErrorResponse(status.HTTP_403_FORBIDDEN, 
                            "Non puoi accedere al di fuori del suo orario di lavoro.")

                '''
                se la password è scaduta o è passato più del numero di giorni 
                indicati nella chiave di config
                imposto nelle requiredActions di cambiare la password
                '''
                requiredActions = []
                changePwdRequired = isPwdExpired(usrFound.dtPwdChanged)
                if(usrFound.pwdExpired == 1 or changePwdRequired):
                    requiredActions.append(CHG_PWD)
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                        detail={"requiredAction":requiredActions})

                #tutto ok, genero il token e consento l'accesso
                # jwt token = id, email, username
                if IsNullOrEmpyStr(ULTE_USER_LOGIN_TOKEN_EXP):
                    raise RuntimeError('CONFIG KEY NOT FOUND: ULTE')
                expTimeConfig = ULTE_USER_LOGIN_TOKEN_EXP
                tokenBody = {
                    'id': usrFound.id,
                    'email': usrFound.email,
                    'username': usrFound.username,
                    'userType': usrFound.userType
                }
                tokenJWT = GenerateToken(expTimeConfig, tokenBody)
                upd_loginAttemptLogs(True, 0, loginAttempt[1], usrFound.id, loginAttempt[1], db, tokenJWT)
                saveJWTToken(usrFound.id, tokenJWT, db)
                res_usrdata1 = UsrData1(
                    usrFound.username, usrFound.email, usrFound.userType,
                    usrFound.dtPwdChanged, usrFound.dtRegistration,
                    usrFound.usabilityTime, usrFound.usabilityDays
                )
                ec = EMailClient()
                if ec != None:
                    background_tasks.add_task(ec.send_login, usrFound.email)
                return ResLogin(
                    userData = res_usrdata1,
                    token = tokenJWT
                )
        else:
            #credenziali errate
            if(loginAttempt[0] == 0):
                #nell'ultimo TIMESPAN di monitoraggio dei login non ci sono state attività di login per questa utenza
                upd_loginAttemptLogs(False, 0, 1, usrFound.id, loginAttempt[2], db)
            else:
                if(loginAttempt[1] <= 5): #se ho già fatto 4 tentativi sbagliati, segno anche il 5°, poi non segno più
                    upd_loginAttemptLogs(False, loginAttempt[0], loginAttempt[1], usrFound.id, loginAttempt[2], db)
                    if loginAttempt[1] == 4:
                        ec = EMailClient()
                        if ec != None:
                            background_tasks.add_task(ec.send_loginFailed5, usrFound.email)
                if(loginAttempt[1] >= 4):
                    #numero di accessi errati superato
                    return CreateErrorResponseHttp(status.HTTP_400_BAD_REQUEST, "La sua utenza e' stata disabilitata per numerosi tentativi di accesso! Reimpostare la password o chiedere aiuto all'assistenza")
            return CreateErrorResponseHttp(status.HTTP_400_BAD_REQUEST, "Le credenziali inserite sono errate")
    else:
        #Utente non trovato
        raise CreateErrorResponse(status.HTTP_400_BAD_REQUEST, "Utenza non registrata! Per effettuare il login è necessario registrarsi")

def saveJWTToken(userId: int, token: str, db: Session):
    '''
    Salvo il token di autenticazione nella tabella Users
    '''
    query = GetQUpdSaveToken({
                'userId': userId,
                'token': token
            })
    db.execute(query.query, query.params)
    db.commit()
    return

def isPwdExpired(dtPwdChanged: datetime) -> bool:
    '''
    Controlla se la pwd del profilo è scaduta, in base all'ultima volta che la pwd è stata modificata
    '''
    ris = False
    if IsNullOrEmpyStr(CPP_CHANGE_PWD_PERIOD):
        raise RuntimeError('CONFIG KEY NOT FOUND: CPP')
    cpp = int(CPP_CHANGE_PWD_PERIOD)
    ris = False
    if dtPwdChanged != None:
        changePwdDay = dtPwdChanged + timedelta(days=cpp)
        if datetime.now() >= changePwdDay:
            ris = True
    return ris

def check_orarioLogin(usabilityTime: str, usabilityDays: str) -> bool:
    '''
    In base al datetime now, controlla se compatibile con l'orario del lavoratore e in base a quello risponde se è possibile proseguire o no
    '''

    # in fase di testing impostare a mano i valori da usare per i test
    dtNow = datetime.now()
    dow = dtNow.weekday()
    hh = 10 # dtNow.hour
    mm = 21 # dtNow.minute

    valid = isDOWValid(dow, usabilityDays)
    if valid:
        valid = isHMValid(hh, mm, usabilityTime)
    
    return valid

def isDOWValid(dow: int, usabilityDays: str) -> bool:
    '''
    Se usabilityDays contiene 7, allora l'accesso è autorizzato tutti i giorni
    Altrimenti usabilityDays riporta i vari giorni in cui è consentito l'accesso
    '''
    valid = True
    if usabilityDays == None or len(usabilityDays) == 0:
        valid = False
    if valid:
        usabilityDaysL = usabilityDays.split(';')
        usabilityDaysL = [int(num1) for num1 in usabilityDaysL]
        if len(usabilityDaysL) > 0:
            if usabilityDaysL[0] != 7 and dow not in usabilityDaysL:
                valid = False
    return valid

def isHMValid(hh: int, mm: int, usabilityTime: str) -> bool:
    valid = True
    if usabilityTime == None or len(usabilityTime) == 0:
        valid = False
    if valid:
        usabilityTimeLStr = usabilityTime.split(';')
        usabilityTimeL = list(map(getTimeListElem, usabilityTimeLStr))
        valid = checkHHMM(usabilityTimeL, hh, mm)
    return valid

def getTimeListElem(orario1: str) -> list:
    '''
    Converte la stringa contenente gli orari in una string di numeri usabile per i confronti
    '''
    tempL = orario1.split('-')
    hhmm1 = tempL[0].split(':')
    minuti = hhmm1[1]
    if int(minuti)<10:
        minuti = '0'+hhmm1[1]
    temp1 = hhmm1[0]+'.'+minuti
    hm1 = float(temp1)
    

    hhmm2 = tempL[1].split(':')
    minuti = hhmm2[1]
    if int(minuti)<10:
        minuti = '0'+hhmm2[1]
    temp1 = hhmm2[0]+'.'+minuti
    hm2 = float(temp1)
    return [hm1,hm2]

def checkHHMM(usabilityTimeL: list, hh: int, mm: int) -> bool:
    if hh < 0 or mm < 0:
        return False
    minuti = str(mm)
    if mm<10:
        minuti = '0'+str(mm)
    temp1 = str(hh)+'.'+minuti
    hmOra = float(temp1)
    return any(
        (min(elem[0], elem[1]) <= hmOra <= max(elem[0], elem[1]))
        for elem in usabilityTimeL
    )

def upd_loginAttemptLogs(loginOK: bool, logAttemptId: int, 
    attemptNum: int, userId: int, prevLoginResult: str, db: Session,
    token: str = None):
    '''
    -Crea il log per indicare il tentativo di accesso
    -Disabilita l'utenza se ci sono stati >= 5 tentativi errati
    '''
    now = datetime.now()
    try:
        if(logAttemptId == 0 or prevLoginResult == 'OK'):
            #creo un nuovo record di log
            query = GetQInsertLogLoginRecord({
                'userId': userId,
                'loginOK': loginOK,
                'now': now,
                'attemptNum': attemptNum,
                'token': token
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
        raise RuntimeError('DB-Q error: SLogin / upd_loginAttemptLogs')

def get_loginAttemptDB(idUsr: int, db: Session):
    '''
    Ritorna il numero di login attempt sbagliati effettuati nell'ultima 1h dall'ultima login positiva
    o in base al tempo indicato dalle configurazioni
    '''
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