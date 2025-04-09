from app.core.config import settings
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from jose import jwt,JWTError
from fastapi import HTTPException,responses
from sqlalchemy.orm import Session
from app.db.models import User
class EmailSchema(BaseModel):
    email:EmailStr

conf = ConnectionConfig(
MAIL_USERNAME ="thufaledhanish@gmail.com",
MAIL_PASSWORD = settings.GOOGLE_APP_KEY,
MAIL_FROM = "thufaledhanish@gmail.com",
MAIL_PORT = 465,
MAIL_SERVER = "smtp.gmail.com",
MAIL_STARTTLS = False,
MAIL_SSL_TLS = True,
USE_CREDENTIALS = True,
VALIDATE_CERTS = True
)

FRONTEND_URL="https://platform.raver.ai/login"

def get_verification_email_html(token: str):
    link = f"http://127.0.0.1:8000/api/v1/auth/verify-email/{token}"
    return f"""
    <p>Thanks for registering!</p>
    <p>Please click the link below to verify your email:</p>
    <a href="{link}">Verify Email</a>
    """

async def simple_send(email: EmailSchema,token:str) -> JSONResponse:
    html= get_verification_email_html(token)
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    try:
       await fm.send_message(message)
       return JSONResponse(status_code=200, content={"message": "email has been sent"}) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

def final_verification(token: str,db:Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user=db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_verified = True
        db.commit()
        db.refresh(user)

      # ✅ Redirect to frontend success page
        return responses.RedirectResponse(url=f"{FRONTEND_URL}/email-verified?status=success")

    except JWTError:
        # ❌ Token is invalid or expired
        return responses.HTMLResponse(
            content="<h2 style='color: red;'>Verification failed. Invalid or expired token.</h2>",
            status_code=401
        )
    except Exception as e:
        # ❌ General error fallback
        return responses.HTMLResponse(
            content=f"<h2 style='color: red;'>An unexpected error occurred: {str(e)}</h2>",
            status_code=500
        )
        raise HTTPException(status_code=401, detail="Invalid token or authentication failed") from e