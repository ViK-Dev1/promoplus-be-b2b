
class ProtectedRoutes:
    # routes that require authentication
    authProtectedRoutes = [
        'ICReactivateUsr',
        'ICChangeUsr',
        'ICChangeEmail'
    ]

    # routes for internal communication
    icProtectedRoutes = [
        'ICReactivateUsr',
        'ICChangeUsr',
        'ICChangeEmail'
    ]

    # routes reserved for super user / admin
    adminProtectedRoutes = [
        'ICReactivateUsr'
    ]