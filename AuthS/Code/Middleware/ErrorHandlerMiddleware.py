from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

from BL.CommonFun import CreateErrorResponse

# ErrorHandlerMiddleware

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except (Exception, RuntimeError) as e:
            if(isinstance(e,AttributeError) or 
               (e.detail != None and 'out of range' in e.detail) or
               e.detail == []):
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
            else:
                return CreateErrorResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, 'ERR-MDLWR')