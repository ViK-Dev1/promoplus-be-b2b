from sqlalchemy import text
from Database.Query import Query

def GetQUpdateReactivateUser(fields: dict) -> Query:
    q1 = text('UPDATE AuthS.Users'+
              ' SET userDisabled = :userDisabled'+
              ' WHERE id = :id')
    p1 = {
        'id': fields['userId'],
        'userDisabled': 0
    }
    return Query(q1,p1)