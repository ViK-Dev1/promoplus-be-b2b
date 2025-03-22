from fastapi import HTTPException, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from BL.CommonFun import IsNullOrEmpyStr

# ICAuthCheckMiddleware

class AdminCheckMiddleware(BaseHTTPMiddleware):
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

            # Extract the username from the token
            auth_header = request.headers.get("Authorization")
            token = auth_header.split(" ")[1]

            sks = ''
            try:
                payload = jwt.decode(token, sks, algorithms=["HS256"])
                username = payload["sub"].get('username')
                #check if the user is an admin (if he has admin in its name) // used just here
                if(username == None
                   or username == ''
                   or 'admin' not in username):
                    return Response(status_code=status.HTTP_403_FORBIDDEN)

            except (Exception, ExpiredSignatureError, InvalidSignatureError) as decodeExcp:
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        
        # If not a protected route, skip to the next code section
        return await call_next(request)
