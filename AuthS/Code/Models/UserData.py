from datetime import datetime

'''
DTO - Più completo e simile all'oggetto presente nel DB
'''
class UserData:
    def __init__(self, 
            id, username, email, pwd, dtRegistration, 
            lastPwd=None, pwdExpired=False, dtPwdChanged=None, 
            tokenChgPwd=None, userDisabledPwd=False, 
            userDisabled=False, usabilityTime=None, 
            usabilityDays=None, token=None, userID_OP=0):
        self.id = id
        self.username = username
        self.email = email
        self.pwd = pwd
        self.lastPwd = lastPwd
        self.pwdExpired = pwdExpired
        self.dtPwdChanged = dtPwdChanged
        self.tokenChgPwd = tokenChgPwd
        self.dtRegistration = dtRegistration
        self.userDisabledPwd = userDisabledPwd
        self.userDisabled = userDisabled
        self.usabilityTime = usabilityTime
        self.usabilityDays = usabilityDays
        self.token = token
        self.userID_OP = userID_OP