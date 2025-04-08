from typing import List

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

class EmailSchema(BaseModel):
    email:EmailStr

conf = ConnectionConfig(
MAIL_USERNAME ="Dhaanish",
MAIL_PASSWORD = "nadhandaleo",
MAIL_FROM = "mohameddhaanish@techmango.net",
MAIL_PORT = 465,
MAIL_SERVER = "mail server",
MAIL_STARTTLS = False,
MAIL_SSL_TLS = True,
USE_CREDENTIALS = True,
VALIDATE_CERTS = True
)

html = """
<p>Thanks for using Fastapi-mail</p> 
"""

async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"}) 