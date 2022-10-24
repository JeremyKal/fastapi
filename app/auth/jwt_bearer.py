from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import decodeJWT
import models
import services



#used to persist authentication on the routes
class JwtBearer(HTTPBearer):
    # enable automatic error reporting
    def __init__(self, auto_Error: bool = True):
        #super().__init__(auto_error=auto_Error) ? super to init inherited class
        super(JwtBearer, self).__init__(auto_error=auto_Error)

    # make instance behave like function and be called like function
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid token")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid token")

    def verify_jwt(self, jwt_token: str) -> bool:
                
        try:
            payload = decodeJWT(jwt_token)
        except:
            payload = None
        return bool(payload)

    