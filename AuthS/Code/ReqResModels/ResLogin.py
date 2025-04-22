from datetime import datetime

class UsrData1:
    def __init__(self, 
        username, email, userType, dtPwdChanged, 
        dtRegistration, usabilityTime, usabilityDays):
        self.username = username
        self.email = email
        self.userType = userType
        self.dtPwdChanged = dtPwdChanged
        self.dtRegistration = dtRegistration
        self.usabilityTime = usabilityTime
        self.usabilityDays = usabilityDays

## Response
class ResLogin:
    def __init__(self, userData: UsrData1, token: str):
        self.userData = userData
        self.token = token

