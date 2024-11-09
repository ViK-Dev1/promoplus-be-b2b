from sqlalchemy import text
from Database.Query import Query

def GetQSelectUser(fields: dict) -> Query:
    q1 = text('SELECT id, username, email, pwd, dtRegistration, userDisabled'+
                 ' FROM AuthS.Users AS a'+
                 ' WHERE a.email = :email'+
                 ' LIMIT 1')
    p1 = {
        'email': fields['email']
    }
    return Query(q1,p1)