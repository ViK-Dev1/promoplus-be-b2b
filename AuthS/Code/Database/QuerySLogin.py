from sqlalchemy import text
from Models.Constants import Tab_LOGLOGINACTIVITIES, Tab_USERS
from Database.Query import Query

def GetQInsertLogLoginRecord(fields: dict) -> Query:
    q1 = text('INSERT INTO '+Tab_LOGLOGINACTIVITIES+' (userId, loginResult, dtLogin, attemptNum, token)'+
                             ' VALUES'+
                             ' (:userId, :loginResult, :dtLogin, :attemptNum, :token)')
    p1 = {
        'userId': fields['userId'],
        'loginResult': "OK" if fields['loginOK'] else "WP",
        'dtLogin': fields['now'],
        'attemptNum': fields['attemptNum'],
        'token': fields['token']
    }
    return Query(q1,p1)

def GetQUpdateLogLoginRecord(fields: dict) -> Query:
    q1 = text('UPDATE '+Tab_LOGLOGINACTIVITIES+
                             ' SET attemptNum = :attemptNum, loginResult = :loginResult, dtLogin = :dtLogin'+
                             ' WHERE id = :id')
    p1 = {
        'id': fields['logAttemptId'],
        'attemptNum': fields['attemptNum'],
        'loginResult': "OK" if fields['loginOK'] else "WP",
        'dtLogin': fields['now']
    }
    return Query(q1,p1)

def GetQUpdateDisableUser(fields: dict) -> Query:
    q1 = text('UPDATE '+Tab_USERS+
                             ' SET userDisabledPwd = :userDisabled'+
                             ' WHERE id = :userId')
    p1 = {
        'userId': fields['userId'],
        'userDisabled': 1
    }
    return Query(q1,p1)

def GetQSelectWrongLoginAttempts(fields: dict) -> Query:
    q1 = text('SELECT logslogin.id, logslogin.loginResult, logslogin.attemptNum' +
            ' FROM '+Tab_USERS+' AS usr' +
            ' INNER JOIN '+Tab_LOGLOGINACTIVITIES+' AS logslogin ON logslogin.userId = usr.id' +
            ' WHERE usr.id = :idUsr AND logslogin.dtLogin >= :timeFrom' +
            ' ORDER BY logslogin.dtLogin DESC' +
            ' LIMIT 1')
    p1 = {
        'idUsr': fields['idUsr'],
        'timeFrom': fields['timeFrom']
    } 
    return Query(q1,p1)

def GetQUpdSaveToken(fields: dict) -> Query:
    q1 = text('UPDATE '+Tab_USERS+
            ' SET token = :token'+
            ' WHERE id = :userId')
    p1 = {
        'userId': fields['userId'],
        'token': fields['token']
    }
    return Query(q1,p1)