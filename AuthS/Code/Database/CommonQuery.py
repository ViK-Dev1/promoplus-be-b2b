from sqlalchemy import text
from Models.Constants import Tab_USERS
from Database.Query import Query

def GetQSelectUser(fields: dict) -> Query:
    q1 = text('SELECT id, username, email, userType, pwd, dtPwdChanged, dtRegistration, '+
                 'pwdExpired, userDisabledPwd, userDisabled, '+
                 'usabilityTime, usabilityDays'+
                 ' FROM '+Tab_USERS+' AS a'+
                 ' WHERE a.email = :email OR a.username = :email'+
                 ' LIMIT 1')
    p1 = {
        'email': fields['email']
    }
    return Query(q1,p1)