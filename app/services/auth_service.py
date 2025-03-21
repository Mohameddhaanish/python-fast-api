from fastapi import security,Depends,HTTPException
from jose import jwt,JWTError
from app.core.config import settings

oauth2_scheme=security.HTTPBearer()

def get_current_user(token: security.HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id:int=payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"user_id": user_id}
    except JWTError :
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data