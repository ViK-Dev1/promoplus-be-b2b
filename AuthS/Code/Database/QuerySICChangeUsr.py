from sqlalchemy import text
from Database.Query import Query

def GetQUpdateUsr(fields: dict) -> Query:
    q1 = text('UPDATE AuthS.Users'+
              ' SET username = :username'+
              ' WHERE id = :id')
    p1 = {
        'id': fields['userId'],
        'username': fields['username']
    }
    return Query(q1,p1)