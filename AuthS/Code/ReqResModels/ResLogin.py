from datetime import datetime

class UsrData1:
    def __init__(self, 
        username, email, dtPwdChanged, 
        dtRegistration, usabilityTime, usabilityDays):
        self.username = username
        self.email = email
        self.dtPwdChanged = dtPwdChanged
        self.dtRegistration = dtRegistration
        self.usabilityTime = usabilityTime
        self.usabilityDays = usabilityDays

## Response
class ResLogin:
    def __init__(self, userData: UsrData1, token: str, requiredAction: list=[]):
        self.userData = userData
        self.token = token
        self.requiredActions = requiredAction

