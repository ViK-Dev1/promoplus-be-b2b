from fastapi import Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from BL.CommonFun import IsNullOrEmpyStr

# UserLoggedAuthCheck

class AuthCheckMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, protectedRoutes: list):
        super().__init__(app)
        self.protectedRoutes = protectedRoutes

    async def dispatch(self, request: Request, call_next):
        # Protected routes list
        protectedRoutesList = self.protectedRoutes
        if(self.protectedRoutes is None):
            self.protectedRoutes == []

        # Get the current route
        current_route = request.scope["path"]
        if(len(current_route)>1):
            current_route = current_route[1:]

        # Check if the route is in our protected routes
        if (current_route in protectedRoutesList):

            # Extract the authorization header
            auth_header = request.headers.get("Authorization")
            
            # Check if the header exists and starts with "Bearer"
            if (not auth_header 
                or not auth_header.startswith("Bearer")
                or len(auth_header.split(' '))!=2
                ):
                return Response(status_code=status.HTTP_401_UNAUTHORIZED)

            # Extract the token from the header
            token = auth_header.split(" ")[1]

            skjwt = ''
            try:
                payload = jwt.decode(token, skjwt, algorithms=["HS256"])
            except (Exception, ExpiredSignatureError, InvalidSignatureError) as decodeExcp:
                #print(decodeExcp) #<----- per verificare perchè non è valido decommentare
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        
        # If it is not a protected route, skip the authorization check
        return await call_next(request)