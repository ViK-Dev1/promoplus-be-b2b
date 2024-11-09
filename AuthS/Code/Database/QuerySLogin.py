from sqlalchemy import text
from Database.Query import Query

def GetQInsertLogLoginRecord(fields: dict) -> Query:
    q1 = text('INSERT INTO AuthS.LogLoginActivity (userId, loginResult, dtLogin, attemptNum)'+
                             ' VALUES'+
                             ' (:userId, :loginResult, :dtLogin, :attemptNum)')
    p1 = {
        'userId': fields['userId'],
        'loginResult': "OK" if fields['loginOK'] else "WP",
        'dtLogin': fields['now'],
        'attemptNum': fields['attemptNum']
    }
    return Query(q1,p1)

def GetQUpdateLogLoginRecord(fields: dict) -> Query:
    q1 = text('UPDATE AuthS.LogLoginActivity'+
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
    q1 = text('UPDATE AuthS.Users'+
                             ' SET userDisabled = :userDisabled'+
                             ' WHERE id = :userId')
    p1 = {
        'userId': fields['userId'],
        'userDisabled': 1
    }
    return Query(q1,p1)

def GetQSelectWrongLoginAttempts(fields: dict) -> Query:
    q1 = text('SELECT logslogin.id, logslogin.loginResult, logslogin.attemptNum' +
            ' FROM AuthS.Users AS usr' +
            ' INNER JOIN AuthS.LogLoginActivity AS logslogin ON logslogin.userId = usr.id' +
            '        AND usr.email = :email' +
            ' WHERE logslogin.dtLogin >= :timeFrom' +
            ' ORDER BY logslogin.dtLogin DESC' +
            ' LIMIT 1')
    p1 = {
        'email': fields['email'],
        'timeFrom': fields['timeFrom']
    } 
    return Query(q1,p1)