# token business

import time
import jwt
from decouple import config


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')

# return generated token
def token_response(token):
    return {
        'access_token': token
    }
    


# sign in token
def signJWT(userID: str):
    payload = {
        'userID': userID,
        'exp': time.time() + 60*60,
        # 'iat': time.time(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


# decode token

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except: 
        return None
