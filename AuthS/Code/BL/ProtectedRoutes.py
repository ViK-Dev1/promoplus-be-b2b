
class ProtectedRoutes:
    # routes that require authentication
    authProtectedRoutes = [] # aggiungere qualcosa se serve

    # routes for internal communication
    icProtectedRoutes = [
        'ICRegisterUsers',
        'ICReactivateUsers',
        'ICDisableUsers',
        'ICChangeUsrData',
        'ICChangeUsrPwd',
        'ICChangeUsersUsabilityTD',
        'provaIC'
    ]

    # routes reserved for super user / admin
    adminProtectedRoutes = [
    ]