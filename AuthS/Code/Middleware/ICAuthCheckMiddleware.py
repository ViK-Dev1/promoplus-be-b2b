from fastapi import HTTPException, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from Config.appsettings import SKS_SECRETKEY_SERVICE
from BL.CommonFun import IsNullOrEmpyStr

# ICAuthCheckMiddleware

class ICAuthCheckMiddleware(BaseHTTPMiddleware):
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

            # Extract the authorization header and serviceName
            auth_header = request.headers.get("AuthorizationS")
            serviceNameH = request.headers.get("serviceName")
            
            # Check if the header exists and starts with "Bearer"
            if (not auth_header 
                or auth_header == ''
                or not auth_header.startswith("Bearer")
                or len(auth_header.split(' '))!=2
                ):
                return Response(status_code=status.HTTP_401_UNAUTHORIZED)
            
            if(serviceNameH == None
               or serviceNameH == ''):
                return Response(status_code=status.HTTP_403_FORBIDDEN)

            # Extract the token from the header
            token = auth_header.split(" ")[1]

            if IsNullOrEmpyStr(SKS_SECRETKEY_SERVICE):
                raise RuntimeError('CONFIG KEY NOT FOUND: SKS')
            sks = SKS_SECRETKEY_SERVICE
            try:
                payload = jwt.decode(token, sks, algorithms=["HS256"])
                serviceNameTkn = payload["sub"].get('serviceName')
                if(serviceNameTkn == None
                   or serviceNameTkn == ''
                   or serviceNameTkn != serviceNameH):
                    return Response(status_code=status.HTTP_403_FORBIDDEN)

            except (Exception, ExpiredSignatureError, InvalidSignatureError) as decodeExcp:
                #print(decodeExcp) #<----- per verificare perchè non è valido decommentare
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        
        # If not a protected route, skip the authorization check
        return await call_next(request)