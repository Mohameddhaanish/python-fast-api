import jwt
from fastapi import Request, HTTPException
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY  # ✅ Ensure this matches the key used for encoding

def verify_token(request: Request):
    
    token = request.cookies.get("access_token")  # ✅ Extract token from HTTP-only cookies
    
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])
       
        return payload  # ✅ Contains user data like `id` and `email`
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
