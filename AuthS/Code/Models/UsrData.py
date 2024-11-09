from datetime import datetime


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
