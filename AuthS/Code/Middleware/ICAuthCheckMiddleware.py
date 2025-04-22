from fastapi import HTTPException, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError
from Config.appsettings import SKS_SECRETKEY_SERVICE
from BL.CommonFun import IsNullOrEmpyStr, ReadToken

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

            # Estraggo gli headers che mi servono
            auth_header = request.headers.get("AuthorizationS")
            serviceNameH = request.headers.get("ServiceName")
            
            # Controllo gli headers recuperati
            if (auth_header == None 
                or auth_header.strip() == ''
                or not auth_header.startswith("Bearer")
                or len(auth_header.split(' ')) !=2):
                return Response(status_code=status.HTTP_403_FORBIDDEN)
            
            if(serviceNameH == None
               or serviceNameH.strip() == ''):
                return Response(status_code=status.HTTP_403_FORBIDDEN)

            # Extract the token from the header
            jwt_token = auth_header.split(" ")[1]
            
            try:
                payload = ReadToken(jwt_token)

                if payload is not None:
                    payloadDict = eval(payload["sub"])
                    serviceNameTkn = payloadDict.get('serviceName')
                    if(serviceNameTkn == None
                    or serviceNameTkn == ''
                    or serviceNameTkn != serviceNameH):
                        return Response(status_code=status.HTTP_403_FORBIDDEN)
                
            except (Exception, ExpiredSignatureError, InvalidSignatureError) as decodeExcp:
                return Response(status_code=status.HTTP_403_FORBIDDEN)
        
        # Se non è una route protetta o se passa i controlli, proseguo
        return await call_next(request)