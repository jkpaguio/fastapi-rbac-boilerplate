from fastapi import  HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials

import jwt
import os

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login")
http_basic = HTTPBasic()

async def get_oauth2_password_bearer(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token directly without splitting
        payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=['HS512'])
        user_values = payload.get('values', {})

        user_id = user_values.get('userid')
        user_level = user_values.get('userlevel')
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="User ID missing in token")
        return {"user_id":user_id, "user_level" : user_level}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

