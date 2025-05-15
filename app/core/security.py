from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.api.v1.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Middleware for Protected Routes
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
